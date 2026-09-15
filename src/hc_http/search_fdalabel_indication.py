"""Search FDA labels by indication via the HC platform API."""

from __future__ import annotations

from typing import Any

import httpx

from hc_http.hc_api_base_url import hc_api_base_url
from hc_http.hc_bearer_headers import hc_bearer_headers
from model.fda_scrape_versions import FdaScrapeVersions

DEFAULT_CACHE_KEY = "2026-03-01"
DEFAULT_SORT_BY = "relevance"


def run_search_fdalabel_indication(
    indication: str,
    *,
    versions: FdaScrapeVersions | None = None,
    maxn: int = 30,
    offset: int = 0,
    limit: int = 10,
    sort_by: str = DEFAULT_SORT_BY,
    cache_key: str = DEFAULT_CACHE_KEY,
) -> list[dict[str, Any]]:
    """POST /fdalabels/search_by_indication and return matching FDA labels."""
    body = (versions or FdaScrapeVersions()).model_dump()
    url = f"{hc_api_base_url()}/fdalabels/search_by_indication"
    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                url,
                params={
                    "indication": indication,
                    "maxn": maxn,
                    "offset": offset,
                    "limit": limit,
                    "sort_by": sort_by,
                    "cache_key": cache_key,
                },
                json=body,
                headers=hc_bearer_headers(),
            )
    except httpx.RequestError as exc:
        raise RuntimeError(f"HC API request failed: {exc}") from exc
    if response.status_code >= 400:
        raise RuntimeError(
            f"HC API search_by_indication failed "
            f"({response.status_code}): {response.text}"
        )
    data = response.json()
    if not isinstance(data, list):
        raise RuntimeError(f"Unexpected HC API response type: {type(data).__name__}")
    return data
