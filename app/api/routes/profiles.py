from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, get_optional_current_user
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


@router.get(
    "",
    operation_id="GetProfileByUsername",
    summary="Get a profile",
    description="Get a profile of a user of the system. Auth is optional",
    response_model=ProfileResponse,
)
def get(
    username: str = Path(..., description="Username of the profile to get"),
    current_user: User = Depends(get_optional_current_user),
    db: Session = Depends(get_db),
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
    username: str = Path(..., description="Username of the profile you want to follow"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
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
    username: str = Path(
        ..., description="Username of the profile you want to unfollow"
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProfileResponse:
    user = _get_profile_from_username(db, username)
    users.follow(db, db_obj=user, follower=current_user, follow=False)
    return ProfileResponse(profile=user.profile(current_user))
