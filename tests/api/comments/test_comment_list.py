from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.comment import Comment
from tests.conftest import create_john_user, generate_article


def test_cannot_list_all_comments_of_non_existent_article(client: TestClient) -> None:
    r = client.get("/api/articles/test-title/comments")
    assert r.status_code == status.HTTP_404_NOT_FOUND


async def test_can_list_all_comments_of_article(client: TestClient, db: AsyncSession) -> None:
    john = await create_john_user(db)

    db_obj = generate_article(john)
    for i in range(1, 6):
        db_obj.comments.append(Comment(body=f"Comment {i}", author=john))
    db.add(db_obj)
    await db.commit()

    r = client.get("/api/articles/test-title/comments")
    assert r.status_code == status.HTTP_200_OK
    assert len(r.json()["comments"]) == 5
    assert {
        "body": "Comment 5",
        "author": {
            "username": "John Doe",
            "bio": "John Bio",
            "image": "https://randomuser.me/api/portraits/men/1.jpg",
            "following": False,
        },
    }.items() <= r.json()["comments"][0].items()
