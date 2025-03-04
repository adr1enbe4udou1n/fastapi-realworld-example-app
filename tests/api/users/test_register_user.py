import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.user import User
from tests.conftest import create_john_user


@pytest.mark.parametrize(
    "data",
    (
        {
            "username": "John Doe",
            "email": "john.doe",
            "password": "password",
        },
        {
            "email": "john.doe@example.com",
        },
        {
            "username": "John Doe",
            "email": "john.doe@example.com",
            "password": "pass",
        },
        {
            "username": "",
            "email": "john.doe@example.com",
            "password": "password",
        },
        {
            "username": "John Doe",
            "email": "john.doe@example.com",
            "password": "",
        },
    ),
)
def test_cannot_register_with_invalid_data(client: TestClient, data: dict[str, str]) -> None:
    r = client.post("/api/users", json={"user": data})

    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_cannot_register_twice(client: TestClient, db: AsyncSession) -> None:
    await create_john_user(db)

    r = client.post(
        "/api/users",
        json={
            "user": {
                "username": "John Doe",
                "email": "john.doe@example.com",
                "password": "password",
            }
        },
    )

    assert r.status_code == status.HTTP_400_BAD_REQUEST


async def test_can_register(client: TestClient, db: AsyncSession) -> None:
    r = client.post(
        "/api/users",
        json={
            "user": {
                "username": "John Doe",
                "email": "john.doe@example.com",
                "password": "password",
            }
        },
    )

    assert r.status_code == status.HTTP_200_OK
    assert (await db.scalar(select(User).filter_by(email="john.doe@example.com"))) is not None
