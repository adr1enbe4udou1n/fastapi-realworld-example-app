from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table

from app.core import security
from app.db.base_class import Base
from app.schemas.profiles import Profile as ProfileDto
from app.schemas.users import User as UserDto

follower_user = Table(
    "follower_user",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("following_id", Integer, ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String)
    bio = Column(Text)
    image = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    followers = relationship(
        "User",
        secondary=follower_user,
        primaryjoin=id == follower_user.c.following_id,
        secondaryjoin=id == follower_user.c.follower_id,
        backref="following",
        uselist=True,
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
