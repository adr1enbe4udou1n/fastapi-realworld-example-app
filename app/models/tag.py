from typing import TYPE_CHECKING, List

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from app.db.base_class import Base
from app.models.article import article_tag

if TYPE_CHECKING:
    from app.models.article import Article  # noqa


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String, nullable=False, unique=True, index=True)

    articles: Mapped[List["Article"]] = relationship(
        "Article",
        back_populates="tags",
        secondary=article_tag,
    )
