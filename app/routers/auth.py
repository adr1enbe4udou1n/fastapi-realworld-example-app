from fastapi import APIRouter
from fastapi.params import Body, Depends

from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from app.dependencies import get_token_header

from app.schemas.users import UpdateUserRequest, User, UserResponse

router = APIRouter(
    prefix="/user",
    tags=["users"],
    dependencies=[Depends(get_token_header)],
)

user = User(
    username="John Doe",
    email="john.doe@example.com",
    bio="John Bio",
    image="https://randomuser.me/api/portraits/men/1.jpg",
    token="secret token",
)


@router.get(
    "/",
    response_model=UserResponse,
)
async def current() -> UserResponse:
    return UserResponse(user)


@router.put(
    "/",
    response_model=UserResponse,
)
async def update(
    user_update: UpdateUserRequest = Body,
) -> UserResponse:
    return UserResponse(user)
