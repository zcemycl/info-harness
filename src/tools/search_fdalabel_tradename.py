"""Search FDA labels by tradename via the HC platform API."""

from __future__ import annotations

from typing import Any

import httpx

from model.fda_scrape_versions import FdaScrapeVersions
from tools.hc_api_base_url import hc_api_base_url
from tools.hc_bearer_headers import hc_bearer_headers


def run_search_fdalabel_tradename(
    tradename: str,
    *,
    versions: FdaScrapeVersions | None = None,
    maxn: int = 30,
    offset: int = 0,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """POST /fdalabels/search_by_tradename and return matching FDA labels."""
    body = (versions or FdaScrapeVersions()).model_dump()
    url = f"{hc_api_base_url()}/fdalabels/search_by_tradename"
    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                url,
                params={
                    "tradename": tradename,
                    "maxn": maxn,
                    "offset": offset,
                    "limit": limit,
                },
                json=body,
                headers=hc_bearer_headers(),
            )
    except httpx.RequestError as exc:
        raise RuntimeError(f"HC API request failed: {exc}") from exc
    if response.status_code >= 400:
        raise RuntimeError(
            f"HC API search_by_tradename failed "
            f"({response.status_code}): {response.text}"
        )
    data = response.json()
    if not isinstance(data, list):
        raise RuntimeError(f"Unexpected HC API response type: {type(data).__name__}")
    return data
