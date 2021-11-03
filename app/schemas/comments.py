import datetime
from typing import List

from pydantic import BaseModel

from app.schemas.profiles import Profile


class NewComment(BaseModel):
    body: str


class NewCommentRequest(BaseModel):
    comment: NewComment


class Comment(BaseModel):
    id: int
    body: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    author: Profile


class SingleCommentResponse(BaseModel):
    comment: Comment


class MultipleCommentsResponse(BaseModel):
    comments: List[Comment]
