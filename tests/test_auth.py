"""
test_auth.py — Módulo Auth
==========================
CP-AUTH-A-001 : Registro retorna HTTP 201 (detecta BUG-01)
CP-AUTH-A-002 : Registro retorna token JWT en el body
CP-AUTH-A-003 : Login retorna token JWT válido
CP-AUTH-A-004 : Login con email inexistente retorna 400
CP-AUTH-A-005 : Registro con email duplicado retorna 400
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession


# ---------------------------------------------------------------------------
# CP-AUTH-A-001
# Nombre   : Registro retorna HTTP 201 Created (no 200)
# Técnica  : EP (partición válida: datos correctos de registro)
# Bug      : BUG-01 — el endpoint retorna 200 en lugar de 201
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_registro_retorna_201(client: TestClient, db: AsyncSession) -> None:
    """CP-AUTH-A-001: POST /api/users con datos válidos debe retornar HTTP 201."""
    payload = {
        "user": {
            "username": "testuser",
            "email": "testuser@test.com",
            "password": "password123",
        }
    }

    response = client.post("/api/users", json=payload)

    assert response.status_code == 201, (
        f"[CP-AUTH-A-001] Se esperaba HTTP 201, se obtuvo {response.status_code}. "
        "Posible BUG-01: el endpoint retorna 200 en lugar de 201."
    )


# ---------------------------------------------------------------------------
# CP-AUTH-A-002
# Nombre   : Registro retorna token JWT en el body
# Técnica  : EP (partición válida)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_registro_retorna_token_jwt(client: TestClient, db: AsyncSession) -> None:
    """CP-AUTH-A-002: POST /api/users debe incluir un token JWT en la respuesta."""
    payload = {
        "user": {
            "username": "testuser2",
            "email": "testuser2@test.com",
            "password": "password123",
        }
    }

    response = client.post("/api/users", json=payload)
    body = response.json()

    assert "user" in body, "[CP-AUTH-A-002] La respuesta no contiene la clave 'user'."
    assert "token" in body["user"], (
        "[CP-AUTH-A-002] La respuesta no contiene un token JWT en 'user.token'."
    )
    token = body["user"]["token"]
    assert isinstance(token, str) and len(token) > 10, (
        f"[CP-AUTH-A-002] El token JWT parece inválido: '{token}'."
    )


# ---------------------------------------------------------------------------
# CP-AUTH-A-003
# Nombre   : Login retorna token JWT válido
# Técnica  : EP (partición válida: credenciales correctas)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_login_retorna_token_jwt(client: TestClient, db: AsyncSession) -> None:
    """CP-AUTH-A-003: POST /api/users/login con credenciales válidas retorna token JWT."""
    # Precondición: registrar el usuario primero
    register_payload = {
        "user": {
            "username": "loginuser",
            "email": "loginuser@test.com",
            "password": "password123",
        }
    }
    client.post("/api/users", json=register_payload)

    # Acción: hacer login
    login_payload = {
        "user": {
            "email": "loginuser@test.com",
            "password": "password123",
        }
    }
    response = client.post("/api/users/login", json=login_payload)
    body = response.json()

    assert response.status_code == 200, (
        f"[CP-AUTH-A-003] Se esperaba HTTP 200, se obtuvo {response.status_code}."
    )
    assert "user" in body, "[CP-AUTH-A-003] La respuesta no contiene la clave 'user'."
    assert "token" in body["user"], (
        "[CP-AUTH-A-003] La respuesta no contiene un token JWT en 'user.token'."
    )
    token = body["user"]["token"]
    assert isinstance(token, str) and len(token) > 10, (
        f"[CP-AUTH-A-003] El token JWT parece inválido: '{token}'."
    )


# ---------------------------------------------------------------------------
# CP-AUTH-A-004
# Nombre   : Login con email inexistente retorna 400
# Técnica  : EP (partición inválida: email que no existe en BD)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_login_email_inexistente_retorna_400(
    client: TestClient, db: AsyncSession
) -> None:
    """CP-AUTH-A-004: POST /api/users/login con email que no existe debe retornar HTTP 400."""
    payload = {
        "user": {
            "email": "noexiste@test.com",
            "password": "cualquierpassword",
        }
    }

    response = client.post("/api/users/login", json=payload)

    assert response.status_code == 400, (
        f"[CP-AUTH-A-004] Se esperaba HTTP 400, se obtuvo {response.status_code}."
    )


# ---------------------------------------------------------------------------
# CP-AUTH-A-005
# Nombre   : Registro con email duplicado retorna 400
# Técnica  : EP (partición inválida: email ya registrado)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_registro_email_duplicado_retorna_400(
    client: TestClient, db: AsyncSession
) -> None:
    """CP-AUTH-A-005: POST /api/users con email ya registrado debe retornar HTTP 400."""
    payload = {
        "user": {
            "username": "usuario_original",
            "email": "duplicado@test.com",
            "password": "password123",
        }
    }

    # Primer registro — debe funcionar
    first_response = client.post("/api/users", json=payload)
    assert first_response.status_code in (200, 201), (
        f"[CP-AUTH-A-005] El primer registro falló inesperadamente con {first_response.status_code}."
    )

    # Segundo registro con el mismo email — debe fallar con 400
    duplicate_payload = {
        "user": {
            "username": "usuario_copia",
            "email": "duplicado@test.com",  # mismo email
            "password": "otropassword",
        }
    }
    response = client.post("/api/users", json=duplicate_payload)

    assert response.status_code == 400, (
        f"[CP-AUTH-A-005] Se esperaba HTTP 400 para email duplicado, "
        f"se obtuvo {response.status_code}."
    )

