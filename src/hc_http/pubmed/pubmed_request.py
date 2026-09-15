"""Shared JSON GET helper for NCBI E-utilities."""

from __future__ import annotations

from typing import Any

import httpx

from hc_http.pubmed.pubmed_env import pubmed_api_key, pubmed_base_url


def pubmed_request_json(
    path: str,
    *,
    params: dict[str, Any],
    timeout: float = 60.0,
) -> Any:
    """GET an E-utilities path and return parsed JSON."""
    query = dict(params)
    query.setdefault("retmode", "json")
    api_key = pubmed_api_key()
    if api_key:
        query["api_key"] = api_key
    url = f"{pubmed_base_url()}{path}"
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.get(url, params=query)
    except httpx.RequestError as exc:
        raise RuntimeError(f"PubMed request failed: {exc}") from exc
    if response.status_code >= 400:
        raise RuntimeError(
            f"PubMed GET {path} failed ({response.status_code}): {response.text}"
        )
    return response.json()
