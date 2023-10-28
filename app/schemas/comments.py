from pydantic import Field

from app.schemas.base import BaseModel
from app.schemas.profiles import Profile


class NewComment(BaseModel):
    body: str = Field(min_length=1)


class NewCommentRequest(BaseModel):
    comment: NewComment


class Comment(BaseModel):
    id: int
    body: str
    created_at: str
    updated_at: str
    author: Profile


class SingleCommentResponse(BaseModel):
    comment: Comment


class MultipleCommentsResponse(BaseModel):
    comments: list[Comment]
