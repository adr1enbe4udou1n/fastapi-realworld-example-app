from typing import Optional

from app.schemas.base import BaseModel


class Profile(BaseModel):
    username: str
    bio: Optional[str] = None
    image: Optional[str] = None
    following: bool


class ProfileResponse(BaseModel):
    profile: Profile
