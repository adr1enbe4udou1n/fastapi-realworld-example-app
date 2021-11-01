from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core import security
from app.crud import users
from app.db.session import SessionLocal
from app.schemas.users import User

key_scheme = APIKeyHeader(name="Authorization")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(key_scheme)
) -> User:
    try:
        token_prefix, token = token.split(" ")
        payload = security.decode_access_token(token)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = users.get(db, id=payload["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
