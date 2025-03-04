import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.user import User
from tests.conftest import acting_as_john, create_jane_user


def test_guest_user_cannot_update_infos(client: TestClient) -> None:
    r = client.put("/api/user")

    assert r.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    "data",
    (
        {
            "username": "John Doe",
            "email": "john.doe",
            "bio": "My Bio",
        },
    ),
)
async def test_user_cannot_update_infos_with_invalid_data(
    client: TestClient, db: AsyncSession, data: dict[str, str]
) -> None:
    await acting_as_john(db, client)

    r = client.put("/api/user", json={"user": data})

    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_user_cannot_update_with_already_used_email(client: TestClient, db: AsyncSession) -> None:
    await create_jane_user(db)
    await acting_as_john(db, client)

    r = client.put("/api/user", json={"user": {"email": "jane.doe@example.com"}})

    assert r.status_code == status.HTTP_400_BAD_REQUEST


async def test_user_can_update_infos(client: TestClient, db: AsyncSession) -> None:
    await acting_as_john(db, client)

    r = client.put(
        "/api/user",
        json={
            "user": {
                "username": "Jane Doe",
                "email": "jane.doe@example.com",
                "bio": "My Bio",
                "image": "https://randomuser.me/api/portraits/men/2.jpg",
            }
        },
    )

    assert r.status_code == status.HTTP_200_OK
    assert {
        "username": "Jane Doe",
        "email": "jane.doe@example.com",
        "bio": "My Bio",
        "image": "https://randomuser.me/api/portraits/men/2.jpg",
    }.items() <= r.json()["user"].items()

    assert (await db.scalar(select(User).filter_by(email="jane.doe@example.com"))) is not None
