from fastapi import APIRouter
from sqlalchemy import select

from app.db.session import SessionLocalRo
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
async def get_list() -> TagsResponse:
    async with SessionLocalRo() as db:
        tags = await db.scalars(select(Tag).order_by(Tag.name))
        return TagsResponse(tags=[tag.name for tag in tags])
