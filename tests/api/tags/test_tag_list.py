from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.tag import Tag


async def test_can_list_all_tags(client: TestClient, db: AsyncSession) -> None:
    db.add(Tag(name="Tag 3"))
    db.add(Tag(name="Tag 2"))
    db.add(Tag(name="Tag 1"))
    await db.commit()

    r = client.get("/api/tags")

    assert r.status_code == status.HTTP_200_OK
    assert r.json()["tags"] == [
        "Tag 1",
        "Tag 2",
        "Tag 3",
    ]
