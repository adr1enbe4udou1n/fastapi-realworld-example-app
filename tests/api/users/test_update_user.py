import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from app.crud.crud_user import users
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
def test_user_cannot_update_infos_with_invalid_data(client: TestClient, db: Session, data: dict[str, str]) -> None:
    acting_as_john(db, client)

    r = client.put("/api/user", json={"user": data})

    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_user_cannot_update_with_already_used_email(client: TestClient, db: Session) -> None:
    create_jane_user(db)
    acting_as_john(db, client)

    r = client.put("/api/user", json={"user": {"email": "jane.doe@example.com"}})

    assert r.status_code == status.HTTP_400_BAD_REQUEST


def test_user_can_update_infos(client: TestClient, db: Session) -> None:
    acting_as_john(db, client)

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

    db_user = users.get_by_email(db, email="jane.doe@example.com")
    assert db_user
