import asyncio
import logging
import os
import sys
from random import choice

from faker import Faker
from slugify import slugify
from sqlalchemy import delete, select

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from sqlalchemy.orm import joinedload

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.article import Article
from app.models.comment import Comment
from app.models.tag import Tag
from app.models.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main() -> None:
    db = SessionLocal()

    logger.info("Cleanup")
    await db.execute(delete(Tag))
    await db.execute(delete(Comment))
    await db.execute(delete(Article))
    await db.execute(delete(User))

    fake = Faker()

    logger.info("Generate 50 users")

    password = get_password_hash("password")

    for _ in range(50):
        user = User(
            name=fake.name(),
            email=fake.email(),
            password=password,
            bio=fake.paragraph(),
            image=f"https://randomuser.me/api/portraits/{choice(['men', 'women'])}/"
            + f"{fake.random_int(min=1, max=99)}.jpg",
        )
        db.add(user)

    await db.commit()

    users = (await db.scalars(select(User).options(joinedload(User.followers)))).unique().all()

    for user in users:
        for _ in range(fake.random_int(min=0, max=3)):
            follower = choice(users)
            if follower not in user.followers:
                user.followers.append(follower)

    await db.commit()

    logger.info("Generate 30 tags")

    for _ in range(30):
        tag = Tag(
            name=f"{fake.unique.word()}",
        )
        db.add(tag)

    await db.commit()

    logger.info("Generate 500 articles")

    tags = (await db.scalars(select(Tag))).all()

    for _ in range(500):
        title = " ".join(fake.words(nb=3))

        article = Article(
            title=title.capitalize(),
            slug=slugify(title),
            description=fake.paragraph(),
            body=" ".join(fake.paragraphs(3)),
        )
        article.author = choice(users)

        for _ in range(fake.random_int(min=0, max=3)):
            tag = choice(tags)
            if tag not in article.tags:
                article.tags.append(tag)

        for _ in range(fake.random_int(min=0, max=5)):
            user = choice(users)
            if user not in article.favorited_by:
                article.favorited_by.append(user)

        db.add(article)

    await db.commit()

    logger.info("Generate 5000 comments")

    articles = (await db.scalars(select(Article))).all()

    for _ in range(5000):
        comment = Comment(body=fake.paragraph(), author=choice(users), article=choice(articles))

        db.add(comment)

    await db.commit()


if __name__ == "__main__":
    asyncio.run(main())
