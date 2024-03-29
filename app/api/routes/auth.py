from fastapi import APIRouter, Body, HTTPException

from app.api.deps import DatabaseSession
from app.crud.crud_user import users
from app.schemas.users import LoginUserRequest, NewUserRequest, UserResponse

router = APIRouter()


@router.post(
    "",
    operation_id="CreateUser",
    summary="Register a new user",
    description="Register a new user",
    response_model=UserResponse,
)
def register(
    db: DatabaseSession,
    new_user: NewUserRequest = Body(...),
) -> UserResponse:
    db_user = users.get_by_email(db, email=new_user.user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = users.create(db, obj_in=new_user.user)
    return UserResponse(user=db_user.schema())


@router.post(
    "/login",
    operation_id="Login",
    summary="Existing user login",
    description="Login for existing user",
    response_model=UserResponse,
)
def login(
    db: DatabaseSession,
    user_credentials: LoginUserRequest = Body(...),
) -> UserResponse:
    db_user = users.authenticate(db, email=user_credentials.user.email, password=user_credentials.user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Bad credentials")
    return UserResponse(user=db_user.schema())
