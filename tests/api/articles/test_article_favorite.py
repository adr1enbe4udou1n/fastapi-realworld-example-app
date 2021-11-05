from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from app.models.article import article_favorite
from tests.conftest import acting_as_john, create_jane_user, generate_article


def test_guest_cannot_favorite_article(client: TestClient) -> None:
    r = client.post("/api/articles/test-title/favorite")
    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_cannot_favorite_non_existent_article(client: TestClient, db: Session) -> None:
    acting_as_john(db, client)
    r = client.post("/api/articles/test-title/favorite")
    assert r.status_code == status.HTTP_404_NOT_FOUND


def test_can_favorite_article(client: TestClient, db: Session) -> None:
    john = acting_as_john(db, client)

    db_obj = generate_article(john)
    db.add(db_obj)
    db.commit()

    r = client.post("/api/articles/test-title/favorite")
    assert r.status_code == status.HTTP_200_OK
    assert {
        "title": "Test Title",
        "description": "Test Description",
        "favorited": True,
        "favoritesCount": 1,
    }.items() <= r.json()["article"].items()
    assert db.query(article_favorite).count() == 1


def test_can_unfavorite_article(client: TestClient, db: Session) -> None:
    john = acting_as_john(db, client)
    jane = create_jane_user(db)

    db_obj = generate_article(jane)
    db_obj.favoritedBy.append(john)
    db.add(db_obj)
    db.commit()

    r = client.delete("/api/articles/test-title/favorite")
    assert r.status_code == status.HTTP_200_OK
    assert {
        "title": "Test Title",
        "description": "Test Description",
        "favorited": False,
        "favoritesCount": 0,
    }.items() <= r.json()["article"].items()
    assert db.query(article_favorite).count() == 0
