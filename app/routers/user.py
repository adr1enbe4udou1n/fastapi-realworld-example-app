from fastapi import APIRouter
from fastapi.params import Body, Depends
from sqlalchemy.orm.session import Session

from app.schemas.users import UpdateUserRequest, User, UserResponse
from app.dependencies import get_current_user, get_db

router = APIRouter(
    prefix="/user",
    tags=["User and Authentication"],
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
    summary="Get current user",
    description="Gets the currently logged-in user",
    response_model=UserResponse
)
async def current(user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse(user=user)


@router.put(
    "/",
    summary="Update current user",
    description="Updated user information for current user",
    response_model=UserResponse
)
async def update(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    user_update: UpdateUserRequest = Body(...),
) -> UserResponse:
    return UserResponse(user=user)
