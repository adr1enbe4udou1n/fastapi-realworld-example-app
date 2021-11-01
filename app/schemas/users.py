from typing import Optional, Annotated

from pydantic import BaseModel, EmailStr, HttpUrl, Field


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class LoginUserRequest(BaseModel):
    user: LoginUser


class NewUser(BaseModel):
    email: EmailStr
    username: str
    password: Annotated[str, Field(min_length=8)]


class NewUserRequest(BaseModel):
    user: NewUser


class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    image: Optional[HttpUrl] = None


class UpdateUserRequest(BaseModel):
    user: UpdateUser


class User(BaseModel):
    username: str
    email: str
    bio: Optional[str] = None
    image: Optional[HttpUrl] = None
    token: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: User
