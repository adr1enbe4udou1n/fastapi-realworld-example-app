from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from app.models.user import follower_user
from tests.conftest import (acting_as_jane, acting_as_user, create_jane_user,
                            create_john_user)


def test_cannot_follow_profile(client: TestClient, db: Session) -> None:
    create_john_user(db)

    r = client.post("/api/profiles/celeb_John Doe/follow")

    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_cannot_follow_non_existent_profile(client: TestClient, db: Session) -> None:
    acting_as_jane(db, client)

    r = client.post("/api/profiles/celeb_John Doe/follow")

    assert r.status_code == status.HTTP_404_NOT_FOUND


def test_can_follow_profile(client: TestClient, db: Session) -> None:
    create_john_user(db)
    acting_as_jane(db, client)

    r = client.post("/api/profiles/celeb_John Doe/follow")

    assert r.status_code == status.HTTP_200_OK
    assert r.json()["profile"] == {
        "username": "John Doe",
        "bio": "John Bio",
        "image": "https://randomuser.me/api/portraits/men/1.jpg",
        "following": True,
    }

    assert db.query(follower_user).count() == 1


def test_can_unfollow_profile(client: TestClient, db: Session) -> None:
    john = create_john_user(db)
    jane = create_jane_user(db)

    john.followers.append(jane)
    db.merge(john)
    db.commit()

    acting_as_user(jane, client)

    r = client.delete("/api/profiles/celeb_John Doe/follow")

    assert r.status_code == status.HTTP_200_OK
    assert r.json()["profile"] == {
        "username": "John Doe",
        "bio": "John Bio",
        "image": "https://randomuser.me/api/portraits/men/1.jpg",
        "following": False,
    }

    assert db.query(follower_user).count() == 0
