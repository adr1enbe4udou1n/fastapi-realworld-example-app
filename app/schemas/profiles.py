from pydantic import HttpUrl

from app.schemas.base import BaseModel


class Profile(BaseModel):
    username: str
    bio: str
    image: HttpUrl
    following: bool


class ProfileResponse(BaseModel):
    profile: Profile
