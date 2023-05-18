from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from tests.conftest import acting_as_user, create_jane_user, create_john_user


def test_cannot_get_non_existent_profile(client: TestClient) -> None:
    r = client.get("/api/profiles/John Doe")

    assert r.status_code == status.HTTP_404_NOT_FOUND


def test_can_get_profile(client: TestClient, db: Session) -> None:
    create_john_user(db)

    r = client.get("/api/profiles/John Doe")

    assert r.status_code == status.HTTP_200_OK

    assert r.json()["profile"] == {
        "username": "John Doe",
        "bio": "John Bio",
        "image": "https://randomuser.me/api/portraits/men/1.jpg",
        "following": False,
    }


def test_can_get_followed_profile(client: TestClient, db: Session) -> None:
    john = create_john_user(db)
    jane = create_jane_user(db)

    john.followers.append(jane)
    db.merge(john)
    db.commit()

    acting_as_user(jane, client)

    r = client.get("/api/profiles/John Doe")

    assert r.status_code == status.HTTP_200_OK

    assert r.json()["profile"] == {
        "username": "John Doe",
        "bio": "John Bio",
        "image": "https://randomuser.me/api/portraits/men/1.jpg",
        "following": True,
    }
