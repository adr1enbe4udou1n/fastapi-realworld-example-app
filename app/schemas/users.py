from typing import Optional

from pydantic import EmailStr, Field

from app.schemas.base import BaseModel


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class LoginUserRequest(BaseModel):
    user: LoginUser


class NewUser(BaseModel):
    email: EmailStr
    username: str = Field(min_length=1)
    password: str = Field(min_length=8)


class NewUserRequest(BaseModel):
    user: NewUser


class UpdateUser(BaseModel):
    username: Optional[str] = Field(min_length=1)
    email: Optional[EmailStr]
    bio: Optional[str]
    image: Optional[str]


class UpdateUserRequest(BaseModel):
    user: UpdateUser


class User(BaseModel):
    username: str
    email: str
    bio: Optional[str] = None
    image: Optional[str] = None
    token: str


class UserResponse(BaseModel):
    user: User
