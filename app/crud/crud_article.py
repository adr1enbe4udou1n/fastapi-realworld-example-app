from typing import Any, Optional

from slugify import slugify
from sqlalchemy.orm import Session

from app.models.article import Article
from app.models.tag import Tag
from app.models.user import User
from app.schemas.articles import NewArticle, UpdateArticle


class ArticlesRepository:
    def get(self, db: Session, id: Any) -> Optional[Article]:
        return db.query(Article).filter(Article.id == id).first()

    def get_by_slug(self, db: Session, *, slug: str) -> Optional[Article]:
        return db.query(Article).filter(Article.slug == slug).first()

    def create(self, db: Session, *, obj_in: NewArticle, author: User) -> Article:
        db_obj = Article(
            title=obj_in.title,
            description=obj_in.description,
            body=obj_in.body,
            slug=slugify(obj_in.title),
            author_id=author.id,
        )

        for tag in obj_in.tag_list:
            db_obj.tags.append(
                db.query(Tag).filter(Tag.name == tag).first() or Tag(name=tag)
            )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Article, obj_in: UpdateArticle) -> Article:
        db_obj.title = obj_in.title or db_obj.title

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, db_obj: Article) -> None:
        db.delete(db_obj)
        db.commit()


articles = ArticlesRepository()
