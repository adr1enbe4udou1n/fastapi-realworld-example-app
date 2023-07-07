from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, relationship

from app.db.base_class import Base
from app.schemas.articles import Article as ArticleDto
from app.schemas.base import convert_datetime_to_realworld

if TYPE_CHECKING:
    from app.models.comment import Comment  # noqa
    from app.models.tag import Tag  # noqa
    from app.models.user import User  # noqa

article_tag: Table = Table(
    "article_tag",
    Base.metadata,
    Column(
        "article_id",
        Integer,
        ForeignKey(
            "articles.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
    Column(
        "tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    ),
)

article_favorite: Table = Table(
    "article_favorite",
    Base.metadata,
    Column(
        "article_id",
        Integer,
        ForeignKey("articles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    ),
)


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    author_id: Mapped[int] = Column(Integer, ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = Column(String, nullable=False)
    slug: Mapped[str] = Column(String, unique=True, nullable=False, index=True)
    description: Mapped[str] = Column(Text, nullable=False)
    body: Mapped[str] = Column(Text, nullable=False)
    created_at: Mapped[datetime] = Column(
        DateTime, default=datetime.now, nullable=False
    )
    updated_at: Mapped[datetime] = Column(
        DateTime, default=datetime.now, nullable=False, onupdate=datetime.now
    )

    author: Mapped["User"] = relationship("User", back_populates="articles")
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="article", uselist=True
    )
    tags: Mapped[List["Tag"]] = relationship(
        "Tag", back_populates="articles", secondary=article_tag, uselist=True
    )
    favorited_by: Mapped[List["User"]] = relationship(
        "User",
        back_populates="favorite_articles",
        secondary=article_favorite,
        uselist=True,
    )

    def schema(self, user: Optional["User"] = None) -> ArticleDto:
        tags = [tag.name for tag in self.tags]
        tags.sort()

        return ArticleDto(
            title=self.title,
            slug=self.slug,
            description=self.description,
            body=self.body,
            created_at=convert_datetime_to_realworld(self.created_at),
            updated_at=convert_datetime_to_realworld(self.updated_at),
            tag_list=tags,
            author=self.author.profile(user),
            favorited=user is not None and self.favorited_by.__contains__(user),
            favorites_count=len(self.favorited_by),
        )
