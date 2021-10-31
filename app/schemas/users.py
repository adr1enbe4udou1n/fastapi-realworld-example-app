from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl


class UserLoginRequest:
    email: EmailStr
    password: str


class NewUserRequest:
    email: EmailStr
    username: str
    password: str


class UserUpdateRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    image: Optional[HttpUrl] = None


class User:
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    image: Optional[HttpUrl] = None
    token: str


class UserResponse:
    user: User
