from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conftest import acting_as_john, generate_article


def test_cannot_get_non_existent_article(client: TestClient) -> None:
    r = client.get("/api/articles/test-title")
    assert r.status_code == status.HTTP_404_NOT_FOUND


async def test_can_get_article(client: TestClient, db: AsyncSession) -> None:
    john = await acting_as_john(db, client)

    db_obj = generate_article(john)
    db.add(db_obj)
    await db.commit()

    r = client.get("/api/articles/test-title")
    assert r.status_code == status.HTTP_200_OK
    assert {
        "title": "Test Title",
        "description": "Test Description",
        "body": "Test Body",
        "author": {
            "username": "John Doe",
            "bio": "John Bio",
            "image": "https://randomuser.me/api/portraits/men/1.jpg",
            "following": False,
        },
        "tagList": [],
        "favorited": False,
        "favoritesCount": 0,
    }.items() <= r.json()["article"].items()
