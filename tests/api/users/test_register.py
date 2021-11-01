from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.crud import users


def test_can_register(client: TestClient, db: Session) -> None:
    r = client.post(
        "/api/users/", json={
            "user": {
                "username": "John Doe",
                "email": "john.doe@example.com",
                "password": "password",
            }
        })

    assert r.status_code == 200

    db_user = users.get_by_email(db, email="john.doe@example.com")
    assert db_user
