from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core import security
from app.db.base_class import Base
from app.models.article import article_favorite
from app.schemas.profiles import Profile as ProfileDto
from app.schemas.users import User as UserDto

if TYPE_CHECKING:
    from app.models.article import Article
    from app.models.comment import Comment


follower_user = Table(
    "follower_user",
    Base.metadata,
    Column(
        "follower_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "following_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password: Mapped[str | None] = mapped_column(String)
    bio: Mapped[str | None] = mapped_column(Text)
    image: Mapped[str | None] = mapped_column(String)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at = mapped_column(DateTime, default=datetime.now, nullable=False, onupdate=datetime.now)

    followers: Mapped[list["User"]] = relationship(
        "User",
        secondary=follower_user,
        primaryjoin=id == follower_user.c.following_id,
        secondaryjoin=id == follower_user.c.follower_id,
        backref="following",
        uselist=True,
    )

    articles: Mapped[list["Article"]] = relationship("Article", back_populates="author")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="author")
    favorite_articles: Mapped[list["Article"]] = relationship(
        "Article",
        back_populates="favorited_by",
        secondary=article_favorite,
    )

    def schema(self) -> UserDto:
        return UserDto(
            username=self.name,
            email=self.email,
            bio=self.bio,
            image=self.image,
            token=security.create_access_token(self.id),
        )

    def profile(self, user: Optional["User"] = None) -> ProfileDto:
        return ProfileDto(
            username=self.name,
            bio=self.bio,
            image=self.image,
            following=user is not None and self.followers.__contains__(user),
        )
