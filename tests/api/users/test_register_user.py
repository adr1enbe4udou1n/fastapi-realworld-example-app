import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.crud.crud_user import users
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

    db_user = await users.get_by_email(db, email="john.doe@example.com")
    assert db_user
