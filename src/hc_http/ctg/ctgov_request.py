"""Shared JSON GET helper for ClinicalTrials.gov API v2."""

from __future__ import annotations

from typing import Any

import httpx

from hc_http.ctg.ctgov_env import ctgov_base_url


def ctgov_request_json(
    path: str,
    *,
    params: dict[str, Any] | None = None,
    timeout: float = 60.0,
) -> Any:
    """GET a CT.gov API v2 path and return parsed JSON."""
    query = dict(params or {})
    query.setdefault("format", "json")
    url = f"{ctgov_base_url()}{path}"
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.get(url, params=query)
    except httpx.RequestError as exc:
        raise RuntimeError(f"CT.gov request failed: {exc}") from exc
    if response.status_code >= 400:
        raise RuntimeError(
            f"CT.gov GET {path} failed ({response.status_code}): {response.text}"
        )
    return response.json()
