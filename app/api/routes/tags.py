from fastapi import APIRouter
from sqlalchemy import select

from app.api.deps import DatabaseRoSession
from app.models.tag import Tag
from app.schemas.tags import TagsResponse

router = APIRouter()


@router.get(
    "",
    operation_id="GetTags",
    summary="Get tags",
    description="Get tags. Auth not required",
    response_model=TagsResponse,
)
async def get_list(
    db: DatabaseRoSession,
) -> TagsResponse:
    tags = await db.scalars(select(Tag).order_by(Tag.name))
    return TagsResponse(tags=[tag.name for tag in tags])
