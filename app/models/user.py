from datetime import datetime
from sqlalchemy import Text, Column, Integer, String, DateTime

from app.schemas.users import User as UserDto
from app.db.base_class import Base
from app.core import security


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

    def schema(self) -> UserDto:
        return UserDto(
            username=self.name,
            email=self.email,
            bio=self.bio,
            image=self.image,
            token=security.create_access_token(self.id),
        )
