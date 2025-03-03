from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.user import follower_user
from tests.conftest import (
    acting_as_jane,
    acting_as_user,
    create_jane_user,
    create_john_user,
)


async def test_cannot_follow_profile(client: TestClient, db: AsyncSession) -> None:
    await create_john_user(db)

    r = client.post("/api/profiles/John Doe/follow")

    assert r.status_code == status.HTTP_403_FORBIDDEN


async def test_cannot_follow_non_existent_profile(client: TestClient, db: AsyncSession) -> None:
    await acting_as_jane(db, client)

    r = client.post("/api/profiles/John Doe/follow")

    assert r.status_code == status.HTTP_404_NOT_FOUND


async def test_can_follow_profile(client: TestClient, db: AsyncSession) -> None:
    await create_john_user(db)
    await acting_as_jane(db, client)

    r = client.post("/api/profiles/John Doe/follow")

    assert r.status_code == status.HTTP_200_OK
    assert r.json()["profile"] == {
        "username": "John Doe",
        "bio": "John Bio",
        "image": "https://randomuser.me/api/portraits/men/1.jpg",
        "following": True,
    }

    assert (await db.scalar(select(follower_user))) is not None


async def test_can_unfollow_profile(client: TestClient, db: AsyncSession) -> None:
    john = await create_john_user(db)
    jane = await create_jane_user(db)

    acting_as_user(jane, client)

    john.followers.append(jane)
    await db.merge(john)
    await db.commit()

    r = client.delete("/api/profiles/John Doe/follow")

    assert r.status_code == status.HTTP_200_OK
    assert r.json()["profile"] == {
        "username": "John Doe",
        "bio": "John Bio",
        "image": "https://randomuser.me/api/portraits/men/1.jpg",
        "following": False,
    }

    assert (await db.scalar(select(follower_user))) is None
