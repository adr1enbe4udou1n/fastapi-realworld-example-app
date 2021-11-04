from typing import Any, Optional

from sqlalchemy.orm import Session

from app.models.article import Article
from app.schemas.articles import NewArticle, UpdateArticle


class ArticlesRepository:
    def get(self, db: Session, id: Any) -> Optional[Article]:
        return db.query(Article).filter(Article.id == id).first()

    def get_by_slug(self, db: Session, *, slug: str) -> Optional[Article]:
        return db.query(Article).filter(Article.slug == slug).first()

    def create(self, db: Session, *, obj_in: NewArticle) -> Article:
        db_obj = Article()
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
