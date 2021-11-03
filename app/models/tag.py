from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.article import article_tag

if TYPE_CHECKING:
    from app.models.article import Article  # noqa


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)

    articles = relationship(
        "Article",
        back_populates="tags",
        secondary=article_tag,
    )
