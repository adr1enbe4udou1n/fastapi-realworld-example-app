from typing import Any

from slugify import slugify
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql.expression import desc

from app.models.article import Article
from app.models.tag import Tag
from app.models.user import User
from app.schemas.articles import NewArticle, UpdateArticle


class ArticlesRepository:
    def get(self, db: Session, id: Any) -> Article | None:
        return db.query(Article).filter_by(id=id).first()

    def get_by_slug(self, db: Session, *, slug: str) -> Article | None:
        return db.query(Article).filter_by(slug=slug).first()

    def get_list(
        self,
        db: Session,
        limit: int,
        offset: int,
        *,
        author: str | None = None,
        tag: str | None = None,
        favorited: str | None = None,
    ) -> tuple[list[Article], int]:
        query = db.query(Article).options(
            joinedload(Article.author),
            joinedload(Article.tags),
            joinedload(Article.favorited_by),
        )

        if author:
            query = query.filter(Article.author.has(User.name.ilike(f"%{author}%")))
        if tag:
            query = query.filter(Article.tags.any(Tag.name.ilike(f"%{tag}%")))
        if favorited:
            query = query.filter(Article.favorited_by.any(User.name.ilike(f"%{favorited}%")))

        return (
            query.order_by(desc(Article.id)).limit(limit).offset(offset).all(),
            query.count(),
        )

    def get_feed(self, db: Session, limit: int, offset: int, *, user: User) -> tuple[list[Article], int]:
        query = (
            db.query(Article)
            .options(
                joinedload(Article.author),
                joinedload(Article.tags),
                joinedload(Article.favorited_by),
            )
            .filter(Article.author.has(User.followers.any(id=user.id)))
        )

        return (
            query.order_by(desc(Article.id)).limit(limit).offset(offset).all(),
            query.count(),
        )

    def create(self, db: Session, *, obj_in: NewArticle, author: User) -> Article:
        db_obj = Article(
            title=obj_in.title,
            description=obj_in.description,
            body=obj_in.body,
            slug=slugify(obj_in.title),
            author_id=author.id,
        )

        for tag in obj_in.tag_list:
            db_obj.tags.append(db.query(Tag).filter_by(name=tag).first() or Tag(name=tag))

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

    def favorite(self, db: Session, *, db_obj: Article, user: User, favorite: bool = True) -> None:
        if favorite:
            db_obj.favorited_by.append(user)
        else:
            db_obj.favorited_by.remove(user)

        db.merge(db_obj)
        db.commit()


articles = ArticlesRepository()
