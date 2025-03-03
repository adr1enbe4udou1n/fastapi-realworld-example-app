import asyncio
from collections.abc import Sequence
from typing import Any

from slugify import slugify
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import desc

from app.models.article import Article
from app.models.tag import Tag
from app.models.user import User
from app.schemas.articles import NewArticle, UpdateArticle


class ArticlesRepository:
    async def get(self, db: AsyncSession, id: Any) -> Article | None:
        return await db.scalar(select(Article).filter_by(id=id))

    async def get_by_slug(self, db: AsyncSession, *, slug: str) -> Article | None:
        return await db.scalar(select(Article).filter_by(slug=slug))

    async def get_list(
        self,
        db: AsyncSession,
        limit: int,
        offset: int,
        *,
        author: str | None = None,
        tag: str | None = None,
        favorited: str | None = None,
    ) -> tuple[Sequence[Article], int]:
        query = select(Article).options(
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

        query_list = query.order_by(desc(Article.id)).limit(limit).offset(offset)
        query_count = select(func.count()).select_from(query.subquery())

        articles, count = await asyncio.gather(db.scalars(query_list), db.scalar(query_count))

        return articles.unique().all(), count or 0

    async def get_feed(self, db: AsyncSession, limit: int, offset: int, *, user: User) -> tuple[Sequence[Article], int]:
        query = (
            select(Article)
            .options(
                joinedload(Article.author),
                joinedload(Article.tags),
                joinedload(Article.favorited_by),
            )
            .filter(Article.author.has(User.followers.any(id=user.id)))
        )

        query_list = query.order_by(desc(Article.id)).limit(limit).offset(offset)
        query_count = select(func.count()).select_from(query.subquery())

        articles, count = await asyncio.gather(db.scalars(query_list), db.scalar(query_count))

        return articles.unique().all(), count or 0

    async def create(self, db: AsyncSession, *, obj_in: NewArticle, author: User) -> Article:
        db_obj = Article(
            title=obj_in.title,
            description=obj_in.description,
            body=obj_in.body,
            slug=slugify(obj_in.title),
            author_id=author.id,
        )

        for tag in obj_in.tag_list:
            db_obj.tags.append(await db.scalar(select(Tag).filter_by(name=tag)) or Tag(name=tag))

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: Article, obj_in: UpdateArticle) -> Article:
        db_obj.title = obj_in.title or db_obj.title
        db_obj.description = obj_in.description or db_obj.description
        db_obj.body = obj_in.body or db_obj.body

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, db_obj: Article) -> None:
        await db.delete(db_obj)
        await db.commit()

    async def favorite(self, db: AsyncSession, *, db_obj: Article, user: User, favorite: bool = True) -> None:
        if favorite:
            (await db_obj.awaitable_attrs.favorited_by).append(user)
        else:
            (await db_obj.awaitable_attrs.favorited_by).remove(user)

        await db.commit()
        await db.refresh(db_obj)


articles = ArticlesRepository()
