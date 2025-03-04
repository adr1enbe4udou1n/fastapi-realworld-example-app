from fastapi import APIRouter, Body, Depends, HTTPException

from app.api.deps import CurrentUser, get_users_service
from app.crud.crud_user import UsersRepository
from app.schemas.users import UpdateUserRequest, UserResponse

router = APIRouter()


@router.get(
    "",
    operation_id="GetCurrentUser",
    summary="Get current user",
    description="Gets the currently logged-in user",
    response_model=UserResponse,
)
async def current(
    current_user: CurrentUser,
) -> UserResponse:
    return UserResponse(user=current_user.schema())


@router.put(
    "",
    operation_id="UpdateCurrentUser",
    summary="Update current user",
    description="Updated user information for current user",
    response_model=UserResponse,
)
async def update(
    current_user: CurrentUser,
    update_user: UpdateUserRequest = Body(...),
    users: UsersRepository = Depends(get_users_service),
) -> UserResponse:
    db_user = await users.get_by_email(email=str(update_user.user.email))
    if db_user and db_user != current_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = await users.update(db_obj=current_user, obj_in=update_user.user)
    return UserResponse(user=db_user.schema())
