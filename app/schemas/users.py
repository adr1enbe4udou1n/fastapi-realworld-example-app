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
    username: str | None = None
    email: EmailStr | None = None
    bio: str | None = None
    image: str | None = None


class UpdateUserRequest(BaseModel):
    user: UpdateUser


class User(BaseModel):
    username: str
    email: str
    bio: str | None = None
    image: str | None = None
    token: str


class UserResponse(BaseModel):
    user: User
