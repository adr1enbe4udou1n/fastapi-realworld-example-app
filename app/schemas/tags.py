from app.schemas.base import BaseModel


class TagsResponse(BaseModel):
    tags: list[str]
