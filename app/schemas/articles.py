from typing import List, Optional

from pydantic import Field

from app.schemas.base import BaseModel
from app.schemas.profiles import Profile


class NewArticle(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    body: str = Field(min_length=1)
    tag_list: List[str] = []


class NewArticleRequest(BaseModel):
    article: NewArticle


class UpdateArticle(BaseModel):
    title: Optional[str] = Field(min_length=1)
    description: Optional[str] = Field(min_length=1)
    body: Optional[str] = Field(min_length=1)


class UpdateArticleRequest(BaseModel):
    article: UpdateArticle


class Article(BaseModel):
    title: str
    slug: str
    description: str
    body: str
    created_at: str
    updated_at: str
    tag_list: List[str]
    author: Profile
    favorited: bool
    favorites_count: int


class SingleArticleResponse(BaseModel):
    article: Article


class MultipleArticlesResponse(BaseModel):
    articles: List[Article]
    articles_count: int
