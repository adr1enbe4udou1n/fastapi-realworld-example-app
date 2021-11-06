from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.schemas.articles import Article as ArticleDto

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

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, nullable=False, onupdate=datetime.now
    )

    author = relationship("User", back_populates="articles")
    comments = relationship("Comment", back_populates="article", uselist=True)
    tags = relationship(
        "Tag", back_populates="articles", secondary=article_tag, uselist=True
    )
    favorited_by = relationship(
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
            created_at=self.created_at,
            updated_at=self.updated_at,
            tag_list=tags,
            author=self.author.profile(user),
            favorited=user is not None and self.favorited_by.__contains__(user),
            favorites_count=len(self.favorited_by),
        )
