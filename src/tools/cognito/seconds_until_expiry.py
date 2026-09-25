"""Read a JWT expiry without verifying the signature."""

from __future__ import annotations

import base64
import json
import time


def seconds_until_expiry(token: str) -> int | None:
    """Return seconds until ``exp``, or ``None`` when the token has no payload."""
    parts = token.split(".")
    if len(parts) < 2:
        return None
    padded = parts[1] + "=" * (-len(parts[1]) % 4)
    try:
        claims = json.loads(base64.urlsafe_b64decode(padded))
    except (ValueError, json.JSONDecodeError):
        return None
    exp = claims.get("exp")
    if not isinstance(exp, int):
        return None
    return exp - int(time.time())
