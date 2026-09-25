"""Build Authorization headers from a live Cognito token."""

from __future__ import annotations

from tools.cognito.bind_access_token import current_access_token
from tools.cognito.refresh_saved_tokens import refresh_saved_tokens
from tools.cognito.seconds_until_expiry import seconds_until_expiry
from tools.load_cognito_tokens import load_cognito_tokens


def hc_bearer_headers() -> dict[str, str]:
    """Use the signed-in chat token, or the CLI file when no request is bound."""
    bound = current_access_token()
    if bound and (seconds_until_expiry(bound) or 0) > 60:
        return _headers(bound)
    return _headers(_file_access_token())


def _file_access_token() -> str:
    saved = load_cognito_tokens().access_token
    if (seconds_until_expiry(saved) or 0) > 60:
        return saved
    return refresh_saved_tokens().access_token


def _headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
