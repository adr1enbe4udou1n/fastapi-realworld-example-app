from typing import Dict

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from app.core.security import decode_access_token, get_password_hash
from app.models.user import User
from tests.conftest import create_john_user


@pytest.mark.parametrize(
    "data",
    (
        {
            "email": "jane.doe@example.com",
            "password": "password",
        },
        {
            "email": "john.doe@example.com",
            "password": "badpawword",
        },
    ),
)
def test_cannot_register_with_invalid_data(
    client: TestClient, db: Session, data: Dict[str, str]
) -> None:
    create_john_user(db)

    r = client.post("/api/users/login", json={"user": data})

    assert r.status_code == status.HTTP_400_BAD_REQUEST


def test_can_login(client: TestClient, db: Session) -> None:
    db_obj = User(
        name="John Doe",
        email="john.doe@example.com",
        password=get_password_hash("password"),
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    r = client.post(
        "/api/users/login",
        json={
            "user": {
                "email": "john.doe@example.com",
                "password": "password",
            }
        },
    )

    assert r.status_code == status.HTTP_200_OK
    assert {
        "username": "John Doe",
        "email": "john.doe@example.com",
    }.items() <= r.json()["user"].items()

    payload = decode_access_token(r.json()["user"]["token"])
    assert int(payload["sub"]) == db_obj.id
