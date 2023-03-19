from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db_ro
from app.models.tag import Tag
from app.schemas.tags import TagsResponse

router = APIRouter()

DatabaseRoSession = Annotated[Session, Depends(get_db_ro)]


@router.get(
    "",
    operation_id="GetTags",
    summary="Get tags",
    description="Get tags. Auth not required",
    response_model=TagsResponse,
)
def get_list(
    db: DatabaseRoSession,
) -> TagsResponse:
    tags = db.query(Tag).order_by(Tag.name).all()
    return TagsResponse(tags=[tag.name for tag in tags])
