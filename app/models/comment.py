from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.schemas.comments import Comment as CommentDto

if TYPE_CHECKING:
    from app.models.article import Article  # noqa
    from app.models.user import User  # noqa


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(
        Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False
    )
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, nullable=False, onupdate=datetime.now
    )

    article = relationship("Article", back_populates="comments")
    author = relationship("User", back_populates="comments")

    def schema(self, user: Optional["User"] = None) -> CommentDto:
        return CommentDto(
            id=self.id,
            body=self.body,
            created_at=self.created_at,
            updated_at=self.updated_at,
            author=self.author.profile(user),
        )
