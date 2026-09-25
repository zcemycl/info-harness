"""Bound chat token wins over the CLI token file."""

from __future__ import annotations

import base64
import json
import time

from hc_http.hc_bearer_headers import hc_bearer_headers
from tools.cognito.bind_access_token import bind_access_token


def test_bound_token_is_sent_without_the_cli_file() -> None:
    token = _jwt(int(time.time()) + 3600)
    with bind_access_token(token):
        headers = hc_bearer_headers()
    assert headers["Authorization"] == f"Bearer {token}"


def _jwt(exp: int) -> str:
    payload = json.dumps({"exp": exp}).encode()
    body = base64.urlsafe_b64encode(payload).decode().rstrip("=")
    return f"header.{body}.sig"
