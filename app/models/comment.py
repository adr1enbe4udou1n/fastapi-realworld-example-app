from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, relationship

from app.db.base_class import Base
from app.schemas.base import convert_datetime_to_realworld
from app.schemas.comments import Comment as CommentDto

if TYPE_CHECKING:
    from app.models.article import Article
    from app.models.user import User


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    article_id: Mapped[int] = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)
    author_id: Mapped[int] = Column(Integer, ForeignKey("users.id"), nullable=False)
    body: Mapped[str] = Column(Text, nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.now, nullable=False, onupdate=datetime.now)

    article: Mapped["Article"] = relationship("Article", back_populates="comments")
    author: Mapped["User"] = relationship("User", back_populates="comments")

    def schema(self, user: Optional["User"] = None) -> CommentDto:
        return CommentDto(
            id=self.id,
            body=self.body,
            created_at=convert_datetime_to_realworld(self.created_at),
            updated_at=convert_datetime_to_realworld(self.updated_at),
            author=self.author.profile(user),
        )
