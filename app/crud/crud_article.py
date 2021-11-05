from typing import Any, Optional

from slugify import slugify
from sqlalchemy.orm import Session

from app.models.article import Article
from app.models.tag import Tag
from app.models.user import User
from app.schemas.articles import NewArticle, UpdateArticle


class ArticlesRepository:
    def get(self, db: Session, id: Any) -> Optional[Article]:
        return db.query(Article).filter_by(id=id).first()

    def get_by_slug(self, db: Session, *, slug: str) -> Optional[Article]:
        return db.query(Article).filter_by(slug=slug).first()

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
                db.query(Tag).filter_by(name=tag).first() or Tag(name=tag)
            )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Article, obj_in: UpdateArticle) -> Article:
        db_obj.title = obj_in.title or db_obj.title
        db_obj.description = obj_in.description or db_obj.description
        db_obj.body = obj_in.body or db_obj.body

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, db_obj: Article) -> None:
        db.delete(db_obj)
        db.commit()

    def favorite(
        self, db: Session, *, db_obj: Article, user: User, favorite: bool = True
    ) -> None:
        if favorite:
            db_obj.favoritedBy.append(user)
        else:
            db_obj.favoritedBy.remove(user)

        db.merge(db_obj)
        db.commit()


articles = ArticlesRepository()
