from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.params import Body, Depends
from pydantic import BaseModel

from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.schemas.users import NewUserRequest, User, UserResponse
from app import config

app = FastAPI()


@app.post(
    "/api/users",
    status_code=HTTP_201_CREATED,
    response_model=UserResponse,
    name="user:register",
)
async def register(
    user_create: NewUserRequest = Body,
) -> UserResponse:
    return UserResponse(
        user=User(
            username='John Doe',
            email='john.doe@example.com',
            bio='John Bio',
            image='https://randomuser.me/api/portraits/men/1.jpg',
            token='secret token',
        ),
    )
