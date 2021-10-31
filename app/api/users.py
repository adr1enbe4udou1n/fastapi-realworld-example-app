from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.params import Body, Depends
from pydantic import BaseModel

from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.schemas.users import NewUserRequest, User, UserResponse
from app import config
from app.services import jwt

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.post(
    "",
    status_code=HTTP_201_CREATED,
    response_model=UserResponse,
    name="user:register",
)
async def register(
    user_create: NewUserRequest = Body(..., embed=True, alias="user"),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserResponse:
    if await check_email_is_taken(users_repo, user_create.email):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.EMAIL_TAKEN,
        )

    user = await users_repo.create_user(**user_create.dict())

    token = jwt.create_access_token_for_user(user, str(config.SECRET_KEY))
    return UserResponse(
        user=User(
            username=user.username,
            email=user.email,
            bio=user.bio,
            image=user.image,
            token=token,
        ),
    )
