from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, get_optional_current_user
from app.crud.crud_user import users
from app.models.user import User
from app.schemas.profiles import ProfileResponse

router = APIRouter()


def get_profile_from_username(
    db: Session,
    username: str,
) -> User:
    db_user = users.get_by_name(db, name=username)
    if not db_user:
        raise HTTPException(status_code=404, detail="No user found")
    return db_user


@router.get(
    "",
    summary="Get a profile",
    description="Get a profile of a user of the system. Auth is optional",
    response_model=ProfileResponse,
)
def get(
    username: str = Path(..., description="Username of the profile to get"),
    current_user: User = Depends(get_optional_current_user),
    db: Session = Depends(get_db),
) -> ProfileResponse:
    user = get_profile_from_username(db, username)
    return ProfileResponse(profile=user.profile(current_user))


@router.post(
    "/follow",
    summary="Follow a user",
    description="Follow a user by username",
    response_model=ProfileResponse,
)
def follow(
    username: str = Path(..., description="Username of the profile you want to follow"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProfileResponse:
    user = get_profile_from_username(db, username)
    user.followers.append(current_user)
    db.merge(user)
    db.commit()

    return ProfileResponse(profile=user.profile(current_user))


@router.delete(
    "/follow",
    summary="Unfollow a user",
    description="Unfollow a user by username",
    response_model=ProfileResponse,
)
def follow(
    username: str = Path(
        ..., description="Username of the profile you want to unfollow"
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProfileResponse:
    user = get_profile_from_username(db, username)
    user.followers.remove(current_user)
    db.merge(user)
    db.commit()

    return ProfileResponse(profile=user.profile(current_user))
