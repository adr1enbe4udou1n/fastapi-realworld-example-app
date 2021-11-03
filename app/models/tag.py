from sqlalchemy import Column, Integer, String

from app.db.base_class import Base
from sqlalchemy.orm import relationship

from app.models.article import Article


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)

    articles = relationship(Article, back_populates="tags")
