from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conftest import acting_as_john


def test_guest_cannot_fetch_infos(client: TestClient) -> None:
    r = client.get("/api/user")

    assert r.status_code == status.HTTP_403_FORBIDDEN


async def test_user_can_fetch_infos(client: TestClient, db: AsyncSession) -> None:
    await acting_as_john(db, client)

    r = client.get("/api/user")

    assert r.status_code == status.HTTP_200_OK
    assert {
        "username": "John Doe",
        "email": "john.doe@example.com",
    }.items() <= r.json()["user"].items()
