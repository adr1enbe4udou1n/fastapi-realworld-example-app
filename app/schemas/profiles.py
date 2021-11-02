from pydantic import BaseModel, HttpUrl


class Profile(BaseModel):
    username: str
    bio: str
    image: HttpUrl
    following: bool


class ProfileResponse(BaseModel):
    profile: Profile
