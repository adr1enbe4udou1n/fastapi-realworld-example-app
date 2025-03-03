from fastapi import APIRouter, HTTPException, Path

from app.api.deps import (
    CurrentUser,
    OptionalCurrentUser,
)
from app.crud.crud_user import users
from app.models.user import User
from app.schemas.profiles import ProfileResponse

router = APIRouter()


async def _get_profile_from_username(
    username: str,
) -> User:
    db_user = await users.get_by_name(name=username)
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
async def get(
    current_user: OptionalCurrentUser,
    username: str = Path(..., description="Username of the profile to get"),
) -> ProfileResponse:
    user = await _get_profile_from_username(username)
    return ProfileResponse(profile=user.profile(current_user))


@router.post(
    "/follow",
    operation_id="FollowUserByUsername",
    summary="Follow a user",
    description="Follow a user by username",
    response_model=ProfileResponse,
)
async def follow(
    current_user: CurrentUser,
    username: str = Path(..., description="Username of the profile you want to follow"),
) -> ProfileResponse:
    user = await _get_profile_from_username(username)
    await users.follow(db_obj=user, follower=current_user)
    return ProfileResponse(profile=user.profile(current_user))


@router.delete(
    "/follow",
    operation_id="UnfollowUserByUsername",
    summary="Unfollow a user",
    description="Unfollow a user by username",
    response_model=ProfileResponse,
)
async def unfollow(
    current_user: CurrentUser,
    username: str = Path(..., description="Username of the profile you want to unfollow"),
) -> ProfileResponse:
    user = await _get_profile_from_username(username)
    await users.follow(db_obj=user, follower=current_user, follow=False)
    return ProfileResponse(profile=user.profile(current_user))
