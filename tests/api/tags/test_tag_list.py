from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from app.models.tag import Tag


def test_can_list_all_tags(client: TestClient, db: Session) -> None:
    db.add(Tag(name="Tag 3"))
    db.add(Tag(name="Tag 2"))
    db.add(Tag(name="Tag 1"))
    db.commit()

    r = client.get("/api/tags")

    assert r.status_code == status.HTTP_200_OK
    assert r.json()["tags"] == [
        "Tag 1",
        "Tag 2",
        "Tag 3",
    ]
