"""Tool: search FDA labels by setid."""

from __future__ import annotations

from typing import Any

from hc_http.fda.search_by_id import run_search_fdalabel_by_id
from model.fda_scrape_versions import FdaScrapeVersions


def search_fdalabel_by_id(
    setids: list[str],
    *,
    versions: FdaScrapeVersions | None = None,
    maxn: int = 30,
    offset: int = 0,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Search FDA labels by one or more setids."""
    return run_search_fdalabel_by_id(
        setids, versions=versions, maxn=maxn, offset=offset, limit=limit
    )
