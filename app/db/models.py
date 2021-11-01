from sqlalchemy import Text, Column, Integer, String, DateTime

from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Base:
    id: int


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
