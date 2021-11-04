from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base

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
