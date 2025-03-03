from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conftest import acting_as_user, create_jane_user, create_john_user


def test_cannot_get_non_existent_profile(client: TestClient) -> None:
    r = client.get("/api/profiles/John Doe")

    assert r.status_code == status.HTTP_404_NOT_FOUND


async def test_can_get_profile(client: TestClient, db: AsyncSession) -> None:
    await create_john_user(db)

    r = client.get("/api/profiles/John Doe")

    assert r.status_code == status.HTTP_200_OK

    assert r.json()["profile"] == {
        "username": "John Doe",
        "bio": "John Bio",
        "image": "https://randomuser.me/api/portraits/men/1.jpg",
        "following": False,
    }


async def test_can_get_followed_profile(client: TestClient, db: AsyncSession) -> None:
    john = await create_john_user(db)
    jane = await create_jane_user(db)

    acting_as_user(jane, client)

    john.followers.append(jane)
    await db.merge(john)
    await db.commit()

    r = client.get("/api/profiles/John Doe")

    assert r.status_code == status.HTTP_200_OK

    assert r.json()["profile"] == {
        "username": "John Doe",
        "bio": "John Bio",
        "image": "https://randomuser.me/api/portraits/men/1.jpg",
        "following": True,
    }
