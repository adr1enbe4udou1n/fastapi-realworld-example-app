from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from app.models.article import Article
from app.models.comment import Comment
from tests.conftest import acting_as_john, create_jane_user, generate_article


def test_guest_cannot_delete_comment(client: TestClient) -> None:
    r = client.delete("/api/articles/test-title/comments/1")
    assert r.status_code == status.HTTP_403_FORBIDDEN


def test_cannot_delete_comment_with_non_existent_article(client: TestClient, db: Session) -> None:
    acting_as_john(db, client)
    r = client.delete("/api/articles/test-title/comments/1")
    assert r.status_code == status.HTTP_404_NOT_FOUND


def test_cannot_delete_non_existent_comment(client: TestClient, db: Session) -> None:
    john = acting_as_john(db, client)

    db_obj = generate_article(john)
    db.add(db_obj)
    db.commit()

    r = client.delete("/api/articles/test-title/comments/1")
    assert r.status_code == status.HTTP_404_NOT_FOUND


def test_cannot_delete_comment_of_other_author(client: TestClient, db: Session) -> None:
    jane = create_jane_user(db)

    db_obj = generate_article(jane)
    comment = Comment(body="Test Comment", author=jane)
    db_obj.comments.append(comment)
    db.add(db_obj)
    db.commit()
    db.refresh(comment)

    acting_as_john(db, client)
    r = client.delete(f"/api/articles/test-title/comments/{comment.id}")
    assert r.status_code == status.HTTP_400_BAD_REQUEST


def test_cannot_delete_comment_with_bad_article(client: TestClient, db: Session) -> None:
    john = acting_as_john(db, client)

    db_obj = Article(
        title="Test Title",
        description="Test Description",
        body="Test Body",
        slug="test-title",
        author=john,
    )
    db.add(db_obj)
    db.commit()

    db_obj = generate_article(john, "other-title")
    comment = Comment(body="Test Comment", author=john)
    db_obj.comments.append(comment)
    db.add(db_obj)
    db.commit()
    db.refresh(comment)

    r = client.delete(f"/api/articles/test-title/comments/{comment.id}")
    assert r.status_code == status.HTTP_400_BAD_REQUEST


def test_can_delete_all_comments_of_own_article(client: TestClient, db: Session) -> None:
    john = acting_as_john(db, client)
    jane = create_jane_user(db)

    db_obj = generate_article(john)
    comment = Comment(body="Test Comment", author=jane)
    db_obj.comments.append(comment)
    db.add(db_obj)
    db.commit()
    db.refresh(comment)

    r = client.delete(f"/api/articles/test-title/comments/{comment.id}")
    assert r.status_code == status.HTTP_200_OK
    assert db.query(Comment).count() == 0


def test_can_delete_own_comment(client: TestClient, db: Session) -> None:
    john = acting_as_john(db, client)
    jane = create_jane_user(db)

    db_obj = generate_article(jane)
    comment = Comment(body="Test Comment", author=john)
    db_obj.comments.append(comment)
    db.add(db_obj)
    db.commit()
    db.refresh(comment)

    r = client.delete(f"/api/articles/test-title/comments/{comment.id}")
    assert r.status_code == status.HTTP_200_OK
    assert db.query(Comment).count() == 0
