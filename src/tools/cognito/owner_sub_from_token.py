"""Read the Cognito subject from an already checked access token."""

from __future__ import annotations

from tools.cognito.seconds_until_expiry import seconds_until_expiry
from tools.cognito.verify_access_token import verify_access_token


def owner_sub_from_token(token: str) -> str:
    """Return ``sub`` from a verified access token."""
    if seconds_until_expiry(token) is None:
        raise ValueError("access token has no expiry")
    claims = verify_access_token(token)
    sub = str(claims.get("sub") or "").strip()
    if not sub:
        raise ValueError("access token has no sub")
    return sub
