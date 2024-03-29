from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import _get_current_user, _get_db
from app.crud.crud_user import users
from app.models.user import User
from app.schemas.users import UpdateUserRequest, UserResponse

router = APIRouter()


@router.get(
    "",
    operation_id="GetCurrentUser",
    summary="Get current user",
    description="Gets the currently logged-in user",
    response_model=UserResponse,
)
def current(
    current_user: User = Depends(_get_current_user),
) -> UserResponse:
    return UserResponse(user=current_user.schema())


@router.put(
    "",
    operation_id="UpdateCurrentUser",
    summary="Update current user",
    description="Updated user information for current user",
    response_model=UserResponse,
)
def update(
    db: Session = Depends(_get_db),
    current_user: User = Depends(_get_current_user),
    update_user: UpdateUserRequest = Body(...),
) -> UserResponse:
    db_user = users.get_by_email(db, email=str(update_user.user.email))
    if db_user and db_user != current_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = users.update(db, db_obj=current_user, obj_in=update_user.user)
    return UserResponse(user=db_user.schema())
