"""Require a Cognito access token and expose its subject."""

from __future__ import annotations

from typing import NamedTuple

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from loguru import logger

from tools.cognito.verify_access_token import verify_access_token

_bearer = HTTPBearer(auto_error=False)


class ChatCaller(NamedTuple):
    """Verified access token and the Cognito user it belongs to."""

    token: str
    sub: str


def require_access_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> ChatCaller:
    """Return the bearer token and ``sub`` after JWKS validation."""
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="missing bearer token")
    token = str(credentials.credentials)
    try:
        claims = verify_access_token(token)
    except Exception as exc:
        logger.warning("rejected cognito token: {}: {}", type(exc).__name__, exc)
        raise HTTPException(status_code=401, detail="invalid token") from exc
    sub = str(claims.get("sub") or "").strip()
    if not sub:
        raise HTTPException(status_code=401, detail="invalid token")
    return ChatCaller(token, sub)
