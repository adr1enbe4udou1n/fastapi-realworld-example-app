from fastapi import APIRouter, HTTPException
from fastapi.params import Body, Depends
from sqlalchemy.orm.session import Session

from app.api.deps import get_db
from app.crud import users

from app.schemas.users import LoginUserRequest, NewUserRequest, UserResponse


router = APIRouter()


@router.post(
    "/",
    summary="Register a new user",
    description="Register a new user",
    response_model=UserResponse
)
def register(
    db: Session = Depends(get_db),
    user_new: NewUserRequest = Body(...),
) -> UserResponse:
    db_user = users.get_by_email(db, email=user_new.user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = users.create(db, obj_in=user_new.user)
    return UserResponse(user=db_user.schema())


@router.post(
    "/login",
    summary="Existing user login",
    description="Login for existing user",
    response_model=UserResponse
)
def login(
    db: Session = Depends(get_db),
    user_credentials: LoginUserRequest = Body(...),
) -> UserResponse:
    db_user = users.authenticate(
        db, email=user_credentials.user.email, password=user_credentials.user.password
    )
    if not db_user:
        raise HTTPException(status_code=400, detail="Bad credentials")
    return UserResponse(user=db_user.schema())
