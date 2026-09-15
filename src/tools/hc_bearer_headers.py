"""Build Authorization headers from saved Cognito tokens."""

from __future__ import annotations

from tools.load_cognito_tokens import load_cognito_tokens


def hc_bearer_headers() -> dict[str, str]:
    """Return Bearer headers using the Cognito access token."""
    tokens = load_cognito_tokens()
    return {
        "Authorization": f"Bearer {tokens.access_token}",
        "Accept": "application/json",
    }
