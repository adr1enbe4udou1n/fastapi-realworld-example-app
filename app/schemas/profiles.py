from app.schemas.base import BaseModel


class Profile(BaseModel):
    username: str
    bio: str | None = None
    image: str | None = None
    following: bool


class ProfileResponse(BaseModel):
    profile: Profile
