from fastapi.params import Depends
from fastapi.security import APIKeyHeader
from app.db.database import SessionLocal

from app.schemas.users import User

key_scheme = APIKeyHeader(name="Authorization")

user = User(
    username="John Doe",
    email="john.doe@example.com",
    bio="John Bio",
    image="https://randomuser.me/api/portraits/men/1.jpg",
    token="secret token",
)


def get_current_user(token: str = Depends(key_scheme)) -> User:
    return user


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
