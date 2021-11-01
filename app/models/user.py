from sqlalchemy import Text, Column, Integer, String, DateTime

from app.schemas.users import User as UserResponse
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
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def schema(self) -> UserResponse:
        user = User(
            username=self.name,
            email=self.email,
            bio=self.bio,
            image=self.image,
            token=security.create_access_token(self.id),
        )
