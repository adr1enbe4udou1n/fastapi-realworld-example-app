from fastapi import APIRouter, HTTPException
from fastapi.params import Body, Depends
from sqlalchemy.orm import query
from sqlalchemy.orm.session import Session

from starlette.status import HTTP_201_CREATED
from app.dependencies import get_db

from app.schemas.users import LoginUserRequest, NewUserRequest, User, UserResponse

from app.db.queries import users


router = APIRouter(
    prefix="/users",
    tags=["User and Authentication"],
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
    summary="Register a new user",
    description="Register a new user",
    response_model=UserResponse
)
async def register(
    db: Session = Depends(get_db),
    user_new: NewUserRequest = Body(...),
) -> UserResponse:
    db_user = users.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return UserResponse(users.create_user(db=db, user=user))


@router.post(
    "/login",
    summary="Existing user login",
    description="Login for existing user",
    response_model=UserResponse
)
async def login(
    db: Session = Depends(get_db),
    user_credentials: LoginUserRequest = Body(...),
) -> UserResponse:
    return UserResponse(user=user)
