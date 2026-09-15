"""Tool: search FDA labels by indication."""

from __future__ import annotations

from typing import Any

from hc_http.fda._cache_key import DEFAULT_CACHE_KEY
from hc_http.fda.search_by_indication import (
    DEFAULT_SORT_BY,
    run_search_fdalabel_indication,
)
from model.fda_scrape_versions import FdaScrapeVersions


def search_fdalabel_indication(
    indication: str,
    *,
    versions: FdaScrapeVersions | None = None,
    maxn: int = 30,
    offset: int = 0,
    limit: int = 10,
    sort_by: str = DEFAULT_SORT_BY,
    cache_key: str = DEFAULT_CACHE_KEY,
) -> list[dict[str, Any]]:
    """Search FDA labels by indication text."""
    return run_search_fdalabel_indication(
        indication,
        versions=versions,
        maxn=maxn,
        offset=offset,
        limit=limit,
        sort_by=sort_by,
        cache_key=cache_key,
    )
