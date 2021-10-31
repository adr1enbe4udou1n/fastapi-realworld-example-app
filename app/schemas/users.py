from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl


class UserLogin:
    email: EmailStr
    password: str


class UserLoginRequest:
    user: UserLogin


class NewUser:
    email: EmailStr
    username: str
    password: str


class NewUserRequest:
    user: NewUser


class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    image: Optional[HttpUrl] = None


class UpdateUserRequest:
    user: UpdateUser


class User:
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    image: Optional[HttpUrl] = None
    token: str


class UserResponse:
    user: User
