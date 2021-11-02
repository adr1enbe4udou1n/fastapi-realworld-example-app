from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_optional_current_user
from app.crud.crud_user import users
from app.models.user import User
from app.schemas.profiles import ProfileResponse

router = APIRouter()


def get_profile_from_username(
    db: Session = Depends(get_db),
    username: str = Path(..., description="Username of the profile to get"),
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
    current_user: User = Depends(get_optional_current_user),
    user: User = Depends(get_profile_from_username),
) -> ProfileResponse:
    return ProfileResponse(profile=user.profile(current_user))
