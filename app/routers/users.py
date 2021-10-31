from fastapi import APIRouter
from fastapi.params import Body

from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.schemas.users import LoginUserRequest, NewUserRequest, User, UserResponse


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

user = User(
    username="John Doe",
    email="john.doe@example.com",
    bio="John Bio",
    image="https://randomuser.me/api/portraits/men/1.jpg",
    token="secret token",
)


@router.post(
    "/",
    status_code=HTTP_201_CREATED,
    response_model=UserResponse,
)
async def register(
    user_new: NewUserRequest = Body,
) -> UserResponse:
    return UserResponse(user)


@router.post(
    "/login",
    response_model=UserResponse,
)
async def login(
    user_credentials: LoginUserRequest = Body,
) -> UserResponse:
    return UserResponse(user)
