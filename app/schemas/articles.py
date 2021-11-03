import datetime
from typing import List

from pydantic import BaseModel

from app.schemas.profiles import Profile


class NewArticle(BaseModel):
    title: str
    description: str
    body: str
    tag_list: List[str]


class NewArticleRequest(BaseModel):
    article: NewArticle


class UpdateArticle(BaseModel):
    tags: List[str]


class UpdateArticleRequest(BaseModel):
    tags: UpdateArticle


class Article(BaseModel):
    title: str
    slug: str
    description: str
    body: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    tag_list: List[str]
    author: Profile
    favorited: bool
    favorites_count: int


class SingleArticleResponse(BaseModel):
    article: Article


class MultipleArticlesResponse(BaseModel):
    articles: List[Article]
    articles_count: int
