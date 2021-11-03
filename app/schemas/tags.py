from typing import List

from pydantic import BaseModel


class TagsResponse(BaseModel):
    tags: List[str]
