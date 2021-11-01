import pytest
from typing import Dict
from starlette import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.crud import users
from app.models.user import User
from tests.conftest import create_john_user


@pytest.mark.parametrize("data", [
    (
        {
            "username": "John Doe",
            "email": "john.doe",
            "password": "password",
        },
    ),
    (
        {
            "email": "john.doe@example.com",
        },
    ),
    (
        {
            "username": "John Doe",
            "email": "john.doe@example.com",
            "password": "pass",
        },
    ),
])
def test_cannot_register_with_invalid_data(client: TestClient, data: Dict[str, str]):
    r = client.post(
        "/api/users/", json={
            "user": data
        })

    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_cannot_register_twice(client: TestClient, db: Session):
    create_john_user(db)

    r = client.post(
        "/api/users/", json={
            "user": {
                "username": "John Doe",
                "email": "john.doe@example.com",
                "password": "password",
            }
        })

    assert r.status_code == status.HTTP_400_BAD_REQUEST


def test_can_register(client: TestClient, db: Session):
    r = client.post(
        "/api/users/", json={
            "user": {
                "username": "John Doe",
                "email": "john.doe@example.com",
                "password": "password",
            }
        })

    assert r.status_code == status.HTTP_200_OK

    db_user = users.get_by_email(db, email="john.doe@example.com")
    assert db_user
