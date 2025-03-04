import asyncio
from collections.abc import Sequence
from typing import Any

from slugify import slugify
from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import desc

from app.db.session import SessionLocalRo
from app.models.article import Article
from app.models.tag import Tag
from app.models.user import User
from app.schemas.articles import NewArticle, UpdateArticle


class ArticlesRepository:
    def __init__(self, db: AsyncSession, dbro: AsyncSession):
        self.db = db
        self.dbro = dbro

    async def get(self, id: Any) -> Article | None:
        return await self.dbro.scalar(
            select(Article)
            .options(
                joinedload(Article.tags),
                joinedload(Article.author).joinedload(User.followers),
                joinedload(Article.favorited_by),
            )
            .filter_by(id=id)
        )

    async def get_by_slug(self, *, slug: str) -> Article | None:
        return await self.dbro.scalar(
            select(Article)
            .options(
                joinedload(Article.tags),
                joinedload(Article.author).joinedload(User.followers),
                joinedload(Article.favorited_by),
            )
            .filter_by(slug=slug)
        )

    async def get_list(
        self,
        limit: int,
        offset: int,
        *,
        author: str | None = None,
        tag: str | None = None,
        favorited: str | None = None,
    ) -> tuple[Sequence[Article], int]:
        query = select(Article).options(
            joinedload(Article.author).joinedload(User.followers),
            joinedload(Article.tags),
            joinedload(Article.favorited_by),
        )

        if author:
            query = query.filter(Article.author.has(User.name.ilike(f"%{author}%")))
        if tag:
            query = query.filter(Article.tags.any(Tag.name.ilike(f"%{tag}%")))
        if favorited:
            query = query.filter(Article.favorited_by.any(User.name.ilike(f"%{favorited}%")))

        return await self.get_paginated_list(limit, offset, query)

    async def get_feed(self, limit: int, offset: int, *, user: User) -> tuple[Sequence[Article], int]:
        query = (
            select(Article)
            .options(
                joinedload(Article.author).joinedload(User.followers),
                joinedload(Article.tags),
                joinedload(Article.favorited_by),
            )
            .filter(Article.author.has(User.followers.any(id=user.id)))
        )

        return await self.get_paginated_list(limit, offset, query)

    async def get_paginated_list(
        self, limit: int, offset: int, query: Select[tuple[Article]]
    ) -> tuple[Sequence[Article], int]:
        query_list = query.order_by(desc(Article.id)).limit(limit).offset(offset)

        async with SessionLocalRo() as db_count:
            query_count = select(func.count()).select_from(query.subquery())

            articles, count = await asyncio.gather(self.dbro.scalars(query_list), db_count.scalar(query_count))

        return articles.unique().all(), count or 0

    async def create(self, *, obj_in: NewArticle, author: User) -> Article:
        db_obj = Article(
            title=obj_in.title,
            description=obj_in.description,
            body=obj_in.body,
            slug=slugify(obj_in.title),
            author_id=author.id,
        )

        for tag in obj_in.tag_list:
            db_obj.tags.append(await self.db.scalar(select(Tag).filter_by(name=tag)) or Tag(name=tag))

        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)

        return await self.get(db_obj.id) or db_obj

    async def update(self, *, db_obj: Article, obj_in: UpdateArticle) -> Article:
        db_obj = await self.db.merge(db_obj)
        db_obj.title = obj_in.title or db_obj.title
        db_obj.description = obj_in.description or db_obj.description
        db_obj.body = obj_in.body or db_obj.body

        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)

        return db_obj

    async def delete(self, *, db_obj: Article) -> None:
        db_obj = await self.db.merge(db_obj)
        await self.db.delete(db_obj)
        await self.db.commit()

    async def favorite(self, *, db_obj: Article, user: User, favorite: bool = True) -> None:
        if favorite:
            db_obj.favorited_by.append(user)
        else:
            db_obj.favorited_by.remove(user)

        await self.db.merge(db_obj)
        await self.db.commit()
