from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.article import Article
from tests.conftest import acting_as_john, create_jane_user, generate_article


def test_guest_cannot_update_article(client: TestClient) -> None:
    r = client.put("/api/articles/test-title")
    assert r.status_code == status.HTTP_403_FORBIDDEN


async def test_cannot_update_non_existant_article(client: TestClient, db: AsyncSession) -> None:
    await acting_as_john(db, client)
    r = client.put(
        "/api/articles/test-title",
        json={
            "article": {
                "title": "Test Title",
            }
        },
    )
    assert r.status_code == status.HTTP_404_NOT_FOUND


async def test_cannot_update_article_of_other_author(client: TestClient, db: AsyncSession) -> None:
    jane = await create_jane_user(db)

    db_obj = generate_article(jane)
    db.add(db_obj)
    await db.commit()

    await acting_as_john(db, client)
    r = client.put("/api/articles/test-title", json={"article": {"title": "New Title"}})
    assert r.status_code == status.HTTP_400_BAD_REQUEST


async def test_can_update_own_article(client: TestClient, db: AsyncSession) -> None:
    john = await acting_as_john(db, client)

    db_obj = generate_article(john)
    db.add(db_obj)
    await db.commit()

    r = client.put(
        "/api/articles/test-title",
        json={
            "article": {
                "title": "New Title",
            }
        },
    )
    assert r.status_code == status.HTTP_200_OK
    assert r.json()["article"]["title"] == "New Title"
    assert await db.scalar(select(Article).filter_by(title="New Title")) is not None
