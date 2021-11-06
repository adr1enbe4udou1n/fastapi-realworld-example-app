import logging
import os
import sys

from faker import Faker
from slugify import slugify

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from app.core.security import get_password_hash  # noqa
from app.db.session import SessionLocal  # noqa
from app.models.article import Article  # noqa
from app.models.comment import Comment  # noqa
from app.models.tag import Tag  # noqa
from app.models.user import User  # noqa

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    db = SessionLocal()

    logger.info("Cleanup")
    db.query(Tag).delete()
    db.query(Comment).delete()
    db.query(Article).delete()
    db.query(User).delete()

    fake = Faker()

    logger.info("Generate 50 users")

    password = get_password_hash("password")

    for _ in range(50):
        user = User(
            name=fake.name(),
            email=fake.email(),
            password=password,
            bio=fake.paragraph(),
            image=f"https://randomuser.me/api/portraits/men/{fake.random_int(min=1, max=99)}.jpg",
        )
        db.add(user)

    db.commit()

    users = db.query(User).all()

    for user in users:
        for _ in range(fake.random_int(min=0, max=3)):
            follower = users[fake.random_int(min=0, max=49)]
            if follower not in user.followers:
                user.followers.append(follower)

    db.commit()

    logger.info("Generate 30 tags")

    for _ in range(30):
        tag = Tag(
            name=f"{fake.unique.word()}",
        )
        db.add(tag)

    db.commit()

    logger.info("Generate 500 articles with few comments")

    tags = db.query(Tag).all()

    for _ in range(500):
        title = " ".join(fake.words(nb=3))

        article = Article(
            title=title.capitalize(),
            slug=slugify(title),
            description=fake.paragraph(),
            body=" ".join(fake.paragraphs(3)),
        )
        article.author = users[fake.random_int(min=0, max=49)]

        for _ in range(fake.random_int(min=1, max=3)):
            tag = tags[fake.random_int(min=0, max=29)]
            if tag not in article.tags:
                article.tags.append(tag)

        for _ in range(fake.random_int(min=0, max=10)):
            user = users[fake.random_int(min=0, max=49)]
            if user not in article.favorited_by:
                article.favorited_by.append(user)

        for _ in range(10):
            article.comments.append(
                Comment(
                    body=fake.paragraph(),
                    author=users[fake.random_int(min=0, max=49)],
                )
            )

        db.add(article)

    db.commit()


if __name__ == "__main__":
    main()
