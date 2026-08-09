from fastapi import APIRouter, Body, Depends, HTTPException

from app.api.deps import get_users_service
from app.crud.crud_user import UsersRepository
from app.schemas.users import LoginUserRequest, NewUserRequest, UserResponse

router = APIRouter()


@router.post(
    "",
    operation_id="CreateUser",
    summary="Register a new user",
    description="Register a new user",
    response_model=UserResponse,
)
async def register(
    new_user: NewUserRequest = Body(...),
    users: UsersRepository = Depends(get_users_service),
) -> UserResponse:
    db_user = await users.get_by_email(email=new_user.user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = await users.create(obj_in=new_user.user)
    return UserResponse(user=db_user.schema())


@router.post(
    "/login",
    operation_id="Login",
    summary="Existing user login",
    description="Login for existing user",
    response_model=UserResponse,
)
async def login(
    user_credentials: LoginUserRequest = Body(...),
    users: UsersRepository = Depends(get_users_service),
) -> UserResponse:
    db_user = await users.authenticate(email=user_credentials.user.email, password=user_credentials.user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Bad credentials")
    return UserResponse(user=db_user.schema())
