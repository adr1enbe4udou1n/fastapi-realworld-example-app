from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.schemas.articles import Article as ArticleDto
from app.schemas.base import convert_datetime_to_realworld

if TYPE_CHECKING:
    from app.models.comment import Comment
    from app.models.tag import Tag
    from app.models.user import User

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
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
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
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
)


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, onupdate=datetime.now)

    author: Mapped["User"] = relationship("User", back_populates="articles")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="article", uselist=True)
    tags: Mapped[list["Tag"]] = relationship("Tag", back_populates="articles", secondary=article_tag, uselist=True)
    favorited_by: Mapped[list["User"]] = relationship(
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
