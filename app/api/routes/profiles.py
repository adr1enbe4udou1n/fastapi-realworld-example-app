from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, get_db_ro, get_optional_current_user
from app.crud.crud_user import users
from app.models.user import User
from app.schemas.profiles import ProfileResponse

router = APIRouter()


def _get_profile_from_username(
    db: Session,
    username: str,
) -> User:
    db_user = users.get_by_name(db, name=username)
    if not db_user:
        raise HTTPException(status_code=404, detail="No user found")
    return db_user


DatabaseRoSession = Annotated[Session, Depends(get_db_ro)]
DatabaseSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]
OptionalCurrentUser = Annotated[User, Depends(get_optional_current_user)]


@router.get(
    "",
    operation_id="GetProfileByUsername",
    summary="Get a profile",
    description="Get a profile of a user of the system. Auth is optional",
    response_model=ProfileResponse,
)
def get(
    current_user: OptionalCurrentUser,
    db: DatabaseRoSession,
    username: str = Path(..., description="Username of the profile to get"),
) -> ProfileResponse:
    user = _get_profile_from_username(db, username)
    return ProfileResponse(profile=user.profile(current_user))


@router.post(
    "/follow",
    operation_id="FollowUserByUsername",
    summary="Follow a user",
    description="Follow a user by username",
    response_model=ProfileResponse,
)
def follow(
    current_user: CurrentUser,
    db: DatabaseSession,
    username: str = Path(..., description="Username of the profile you want to follow"),
) -> ProfileResponse:
    user = _get_profile_from_username(db, username)
    users.follow(db, db_obj=user, follower=current_user)
    return ProfileResponse(profile=user.profile(current_user))


@router.delete(
    "/follow",
    operation_id="UnfollowUserByUsername",
    summary="Unfollow a user",
    description="Unfollow a user by username",
    response_model=ProfileResponse,
)
def unfollow(
    current_user: CurrentUser,
    db: DatabaseSession,
    username: str = Path(
        ..., description="Username of the profile you want to unfollow"
    ),
) -> ProfileResponse:
    user = _get_profile_from_username(db, username)
    users.follow(db, db_obj=user, follower=current_user, follow=False)
    return ProfileResponse(profile=user.profile(current_user))
