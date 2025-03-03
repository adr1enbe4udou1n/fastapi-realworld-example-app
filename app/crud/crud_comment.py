from collections.abc import Sequence
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import desc

from app.db.session import SessionLocal, SessionLocalRo
from app.models.article import Article
from app.models.comment import Comment
from app.models.user import User
from app.schemas.comments import NewComment


class CommentsRepository:
    async def get(self, id: Any) -> Comment | None:
        async with SessionLocalRo() as db:
            return await db.scalar(select(Comment).filter_by(id=id))

    async def get_list(self, article: Article) -> Sequence[Comment]:
        async with SessionLocalRo() as db:
            return (
                await db.scalars(
                    select(Comment)
                    .options(joinedload(Comment.author))
                    .filter_by(article=article)
                    .order_by(desc(Comment.id))
                )
            ).all()

    async def create(self, *, obj_in: NewComment, article: Article, author: User) -> Comment:
        async with SessionLocal() as db:
            db_obj = Comment(
                article=article,
                author=author,
                body=obj_in.body,
            )
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj

    async def delete(self, *, db_obj: Comment) -> None:
        async with SessionLocal() as db:
            await db.delete(db_obj)
            await db.commit()


comments = CommentsRepository()
