from typing import Optional

from pydantic import HttpUrl

from app.schemas.base import BaseModel


class Profile(BaseModel):
    username: str
    bio: Optional[str] = None
    image: Optional[HttpUrl] = None
    following: bool


class ProfileResponse(BaseModel):
    profile: Profile
