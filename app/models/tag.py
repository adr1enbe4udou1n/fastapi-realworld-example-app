from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.article import article_tag

if TYPE_CHECKING:
    from app.models.article import Article


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)

    articles: Mapped[list["Article"]] = relationship(
        "Article",
        back_populates="tags",
        secondary=article_tag,
    )
