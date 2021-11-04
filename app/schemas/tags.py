from typing import List

from app.schemas.base import BaseModel


class TagsResponse(BaseModel):
    tags: List[str]
