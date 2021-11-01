from fastapi import APIRouter
from fastapi.params import Body, Depends
from sqlalchemy.orm.session import Session

from app.schemas.users import UpdateUserRequest, User, UserResponse
from app.api.deps import get_current_user, get_db
from app.crud import users

router = APIRouter()


@router.get(
    "/",
    summary="Get current user",
    description="Gets the currently logged-in user",
    response_model=UserResponse
)
def current(current_user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse(user=current_user.schema())


@router.put(
    "/",
    summary="Update current user",
    description="Updated user information for current user",
    response_model=UserResponse
)
def update(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user_update: UpdateUserRequest = Body(...),
) -> UserResponse:
    db_user = users.update(db, db_obj=current_user, obj_in=user_update.user)
    return UserResponse(user=db_user.schema())
