"""Shared HTTP helpers for HC platform JSON requests."""

from __future__ import annotations

from typing import Any

import httpx

from hc_http.hc_api_base_url import hc_api_base_url
from hc_http.hc_bearer_headers import hc_bearer_headers
from tools.cognito.bind_access_token import current_access_token
from tools.cognito.refresh_saved_tokens import refresh_saved_tokens


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
    response = _send(method, url, headers, params, json_body, timeout)
    if auth and _expired(response) and current_access_token() is None:
        fresh = refresh_saved_tokens().access_token
        response = _send(
            method,
            url,
            {
                "Authorization": f"Bearer {fresh}",
                "Accept": "application/json",
            },
            params,
            json_body,
            timeout,
        )
    if response.status_code >= 400:
        raise RuntimeError(
            f"HC API {method.upper()} {path} failed "
            f"({response.status_code}): {response.text}"
        )
    return response.json()


def _send(
    method: str,
    url: str,
    headers: dict[str, str],
    params: dict[str, Any] | None,
    json_body: Any | None,
    timeout: float,
) -> httpx.Response:
    try:
        with httpx.Client(timeout=timeout) as client:
            return client.request(
                method.upper(),
                url,
                params=params,
                json=json_body,
                headers=headers,
            )
    except httpx.RequestError as exc:
        raise RuntimeError(f"HC API request failed: {exc}") from exc


def _expired(response: httpx.Response) -> bool:
    return response.status_code == 401 and "AUTH_EXPIRED" in response.text
