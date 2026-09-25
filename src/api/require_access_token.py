"""Require a Cognito access token on FastAPI routes."""

from __future__ import annotations

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from loguru import logger

from tools.cognito.verify_access_token import verify_access_token

_bearer = HTTPBearer(auto_error=False)


def require_access_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> str:
    """Return the raw access token after JWKS validation."""
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="missing bearer token")
    token = str(credentials.credentials)
    try:
        verify_access_token(token)
    except Exception as exc:
        logger.warning("rejected cognito token: {}: {}", type(exc).__name__, exc)
        raise HTTPException(status_code=401, detail="invalid token") from exc
    return token
