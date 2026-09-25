"""Validate a Cognito access token against the configured user pool."""

from __future__ import annotations

from typing import Any

import jwt
from jwt import PyJWKClient

from model.cognito_config import CognitoConfig

_jwks: PyJWKClient | None = None
_issuer: str | None = None


def verify_access_token(token: str) -> dict[str, Any]:
    """Return claims when ``token`` is an access token for this app client."""
    config = CognitoConfig.from_env()
    issuer = f"https://cognito-idp.{config.region}.amazonaws.com/{config.user_pool_id}"
    signing_key = _client(issuer).get_signing_key_from_jwt(token)
    claims = jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        issuer=issuer,
        leeway=60,
        options={"verify_aud": False},
    )
    if claims.get("token_use") != "access":
        raise ValueError("Cognito token_use must be access")
    if claims.get("client_id") != config.user_pool_client_id:
        raise ValueError("Cognito access token client_id does not match")
    return dict(claims)


def _client(issuer: str) -> PyJWKClient:
    global _jwks, _issuer
    if _jwks is None or _issuer != issuer:
        _issuer = issuer
        _jwks = PyJWKClient(f"{issuer}/.well-known/jwks.json")
    return _jwks
