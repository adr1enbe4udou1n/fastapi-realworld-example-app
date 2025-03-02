from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.article import article_favorite
from tests.conftest import acting_as_john, create_jane_user, generate_article


def test_guest_cannot_favorite_article(client: TestClient) -> None:
    r = client.post("/api/articles/test-title/favorite")
    assert r.status_code == status.HTTP_403_FORBIDDEN


async def test_cannot_favorite_non_existent_article(client: TestClient, db: AsyncSession) -> None:
    await acting_as_john(db, client)
    r = client.post("/api/articles/test-title/favorite")
    assert r.status_code == status.HTTP_404_NOT_FOUND


async def test_can_favorite_article(client: TestClient, db: AsyncSession) -> None:
    john = await acting_as_john(db, client)

    db_obj = generate_article(john)
    db.add(db_obj)
    await db.commit()

    r = client.post("/api/articles/test-title/favorite")
    assert r.status_code == status.HTTP_200_OK
    assert {
        "title": "Test Title",
        "description": "Test Description",
        "favorited": True,
        "favoritesCount": 1,
    }.items() <= r.json()["article"].items()
    assert await db.scalar(select(article_favorite)) is not None


async def test_can_unfavorite_article(client: TestClient, db: AsyncSession) -> None:
    john = await acting_as_john(db, client)
    jane = await create_jane_user(db)

    db_obj = generate_article(jane)
    db_obj.favorited_by.append(john)
    db.add(db_obj)
    await db.commit()

    r = client.delete("/api/articles/test-title/favorite")
    assert r.status_code == status.HTTP_200_OK
    assert {
        "title": "Test Title",
        "description": "Test Description",
        "favorited": False,
        "favoritesCount": 0,
    }.items() <= r.json()["article"].items()
    assert await db.scalar(select(article_favorite)) is None
