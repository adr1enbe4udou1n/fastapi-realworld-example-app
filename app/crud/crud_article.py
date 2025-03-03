import asyncio
from collections.abc import Sequence
from typing import Any

from slugify import slugify
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import desc

from app.db.session import SessionLocal, SessionLocalRo
from app.models.article import Article
from app.models.tag import Tag
from app.models.user import User
from app.schemas.articles import NewArticle, UpdateArticle


class ArticlesRepository:
    async def get(self, id: Any) -> Article | None:
        async with SessionLocalRo() as db:
            return await db.scalar(
                select(Article)
                .options(
                    joinedload(Article.tags),
                    joinedload(Article.author).joinedload(User.followers),
                    joinedload(Article.favorited_by),
                )
                .filter_by(id=id)
            )

    async def get_by_slug(self, *, slug: str) -> Article | None:
        async with SessionLocalRo() as db:
            return await db.scalar(
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

        async with SessionLocalRo() as db1:
            async with SessionLocalRo() as db2:
                articles, count = await asyncio.gather(db1.scalars(query_list), db2.scalar(query_count))

        return articles.unique().all(), count or 0

    async def get_feed(self, limit: int, offset: int, *, user: User) -> tuple[Sequence[Article], int]:
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

        async with SessionLocalRo() as db1:
            async with SessionLocalRo() as db2:
                articles, count = await asyncio.gather(db1.scalars(query_list), db2.scalar(query_count))

        return articles.unique().all(), count or 0

    async def create(self, *, obj_in: NewArticle, author: User) -> Article:
        async with SessionLocal() as db:
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

        return await self.get(db_obj.id) or db_obj

    async def update(self, *, db_obj: Article, obj_in: UpdateArticle) -> Article:
        async with SessionLocal() as db:
            db_obj.title = obj_in.title or db_obj.title
            db_obj.description = obj_in.description or db_obj.description
            db_obj.body = obj_in.body or db_obj.body

            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)

        return await self.get(db_obj.id) or db_obj

    async def delete(self, *, db_obj: Article) -> None:
        async with SessionLocal() as db:
            await db.delete(db_obj)
            await db.commit()

    async def favorite(self, *, db_obj: Article, user: User, favorite: bool = True) -> None:
        async with SessionLocal() as db:
            if favorite:
                db_obj.favorited_by.append(user)
            else:
                db_obj.favorited_by = [fav_user for fav_user in db_obj.favorited_by if fav_user.id != user.id]

            await db.merge(db_obj)
            await db.commit()


articles = ArticlesRepository()
