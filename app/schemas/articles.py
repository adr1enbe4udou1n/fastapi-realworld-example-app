import datetime
from typing import Annotated, List, Optional

from pydantic import Field

from app.schemas.base import BaseModel
from app.schemas.profiles import Profile


class NewArticle(BaseModel):
    title: str
    description: str
    body: str
    tag_list: List[str]


class NewArticleRequest(BaseModel):
    article: NewArticle


class UpdateArticle(BaseModel):
    title: Annotated[Optional[str], Field(min_length=1)] = None
    description: Annotated[Optional[str], Field(min_length=1)] = None
    body: Annotated[Optional[str], Field(min_length=1)] = None


class UpdateArticleRequest(BaseModel):
    article: UpdateArticle


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
