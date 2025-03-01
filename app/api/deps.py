from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, HTTPException, Request, Security, status
from fastapi.security import APIKeyHeader
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.crud.crud_user import users
from app.db.session import SessionLocal, SessionLocalRo
from app.models.user import User


async def _get_db() -> AsyncGenerator:
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def _get_db_ro() -> AsyncGenerator:
    db = SessionLocalRo()
    try:
        yield db
    finally:
        await db.close()


async def _get_current_user_from_token(db: AsyncSession, token: str) -> User:
    try:
        payload = security.decode_access_token(token)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await users.get(db, id=int(payload["sub"]))
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


async def _get_current_user(
    db: AsyncSession = Depends(_get_db), token: str = Depends(_get_authorization_header)
) -> User:
    return await _get_current_user_from_token(db, token)


async def _get_optional_current_user(
    db: AsyncSession = Depends(_get_db),
    token: str = Depends(_get_optional_authorization_header),
) -> User | None:
    if token:
        return await _get_current_user_from_token(db, token)

    return None


DatabaseRoSession = Annotated[AsyncSession, Depends(_get_db_ro)]
DatabaseSession = Annotated[AsyncSession, Depends(_get_db)]
CurrentUser = Annotated[User, Depends(_get_current_user)]
OptionalCurrentUser = Annotated[User, Depends(_get_optional_current_user)]
