import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.comment import Comment
from tests.conftest import acting_as_john, generate_article


def test_guest_cannot_create_comment(client: TestClient) -> None:
    r = client.post("/api/articles/test-title/comments")
    assert r.status_code == status.HTTP_403_FORBIDDEN


async def test_cannot_create_comment_to_non_existent_article(client: TestClient, db: AsyncSession) -> None:
    await acting_as_john(db, client)
    r = client.post("/api/articles/test-title/comments", json={"comment": {"body": "Test Comment"}})
    assert r.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "data",
    (
        {
            "body": "",
        },
    ),
)
async def test_cannot_create_comment_with_invalid_data(
    client: TestClient, db: AsyncSession, data: dict[str, str]
) -> None:
    john = await acting_as_john(db, client)

    db_obj = generate_article(john)
    db.add(db_obj)
    await db.commit()

    r = client.post("/api/articles/test-title/comments", json={"comment": data})
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_can_create_comment(client: TestClient, db: AsyncSession) -> None:
    john = await acting_as_john(db, client)

    db_obj = generate_article(john)
    db.add(db_obj)
    await db.commit()

    r = client.post("/api/articles/test-title/comments", json={"comment": {"body": "Test Comment"}})
    assert r.status_code == status.HTTP_200_OK
    assert r.json()["comment"]["body"] == "Test Comment"
    assert await db.scalar(select(Comment).filter_by(body="Test Comment")) is not None
