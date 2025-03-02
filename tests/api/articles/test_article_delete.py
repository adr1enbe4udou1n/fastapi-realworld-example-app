from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.article import Article
from tests.conftest import acting_as_john, create_jane_user, generate_article


def test_guest_cannot_delete_article(client: TestClient, db: AsyncSession) -> None:
    r = client.delete("/api/articles/test-title")
    assert r.status_code == status.HTTP_403_FORBIDDEN


async def test_cannot_delete_non_existent_article(client: TestClient, db: AsyncSession) -> None:
    await acting_as_john(db, client)
    r = client.delete("/api/articles/test-title")
    assert r.status_code == status.HTTP_404_NOT_FOUND


async def test_cannot_delete_article_of_other_author(client: TestClient, db: AsyncSession) -> None:
    jane = await create_jane_user(db)

    db_obj = generate_article(jane)
    db.add(db_obj)
    await db.commit()

    await acting_as_john(db, client)

    r = client.delete("/api/articles/test-title")
    assert r.status_code == status.HTTP_400_BAD_REQUEST


async def test_can_delete_own_article_with_all_comments(client: TestClient, db: AsyncSession) -> None:
    john = await acting_as_john(db, client)

    db_obj = generate_article(john)
    db.add(db_obj)
    await db.commit()

    r = client.delete("/api/articles/test-title")
    assert r.status_code == status.HTTP_200_OK
    assert await db.scalar(select(Article)) is None
