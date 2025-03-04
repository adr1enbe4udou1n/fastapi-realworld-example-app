from collections.abc import Sequence
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import desc

from app.models.article import Article
from app.models.comment import Comment
from app.models.user import User
from app.schemas.comments import NewComment


class CommentsRepository:
    def __init__(self, db: AsyncSession, dbro: AsyncSession):
        self.db = db
        self.dbro = dbro

    async def get(self, id: Any) -> Comment | None:
        return await self.dbro.scalar(
            select(Comment)
            .options(joinedload(Comment.article), joinedload(Comment.author).joinedload(User.followers))
            .filter_by(id=id)
        )

    async def get_list(self, article: Article) -> Sequence[Comment]:
        return (
            await self.dbro.scalars(
                select(Comment)
                .options(joinedload(Comment.author))
                .filter_by(article=article)
                .order_by(desc(Comment.id))
            )
        ).all()

    async def create(self, *, obj_in: NewComment, article: Article, author: User) -> Comment:
        db_obj = Comment(
            article_id=article.id,
            author_id=author.id,
            body=obj_in.body,
        )
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)

        comment = await self.get(db_obj.id)
        return comment or db_obj

    async def delete(self, *, db_obj: Comment) -> None:
        db_obj = await self.db.merge(db_obj)
        await self.db.delete(db_obj)
        await self.db.commit()
