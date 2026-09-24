"""Shared HTTP helpers for HC platform JSON requests."""

from __future__ import annotations

from typing import Any

import httpx

from hc_http.hc_api_base_url import hc_api_base_url
from hc_http.hc_bearer_headers import hc_bearer_headers


def hc_request_json(
    method: str,
    path: str,
    *,
    params: dict[str, Any] | None = None,
    json_body: Any | None = None,
    timeout: float = 60.0,
    auth: bool = True,
) -> Any:
    """Send a JSON request to `HC_API_BASE_URL` + path and return parsed JSON."""
    url = f"{hc_api_base_url()}{path}"
    headers = hc_bearer_headers() if auth else {"Accept": "application/json"}
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.request(
                method.upper(),
                url,
                params=params,
                json=json_body,
                headers=headers,
            )
    except httpx.RequestError as exc:
        raise RuntimeError(f"HC API request failed: {exc}") from exc
    if response.status_code >= 400:
        raise RuntimeError(
            f"HC API {method.upper()} {path} failed "
            f"({response.status_code}): {response.text}"
        )
    return response.json()
