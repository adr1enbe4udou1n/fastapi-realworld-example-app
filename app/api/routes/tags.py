from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.tag import Tag
from app.schemas.tags import TagsResponse

router = APIRouter()


@router.get(
    "",
    summary="Get tags",
    description="Get tags. Auth not required",
    response_model=TagsResponse,
)
def get_list(
    db: Session = Depends(get_db),
) -> TagsResponse:
    tags = db.query(Tag).order_by(Tag.name).all()
    return TagsResponse(tags=[tag.name for tag in tags])
