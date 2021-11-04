from typing import Generator, Optional

from fastapi import Depends, HTTPException, Request, Security, status
from fastapi.security import APIKeyHeader
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core import security
from app.crud.crud_user import users
from app.db.session import SessionLocal
from app.models.user import User


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _get_current_user(db: Session, token: str) -> User:
    try:
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


def _get_authorization_header(
    api_key: str = Security(
        APIKeyHeader(name="Authorization"),
    ),
) -> str:
    try:
        token_prefix, token = api_key.split(" ")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    return token


def _get_optional_authorization_header(request: Request) -> str:
    authorization = request.headers.get("Authorization")
    if authorization:
        return _get_authorization_header(authorization)

    return ""


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(_get_authorization_header)
) -> User:
    return _get_current_user(db, token)


def get_optional_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(_get_optional_authorization_header),
) -> Optional[User]:
    if token:
        return _get_current_user(db, token)

    return None
