"""Tool: search FDA labels by tradename."""

from __future__ import annotations

from typing import Any

from hc_http.fda.search_by_tradename import run_search_fdalabel_tradename
from model.fda_scrape_versions import FdaScrapeVersions


def search_fdalabel_tradename(
    tradename: str,
    *,
    versions: FdaScrapeVersions | None = None,
    maxn: int = 30,
    offset: int = 0,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Search FDA labels by tradename."""
    return run_search_fdalabel_tradename(
        tradename, versions=versions, maxn=maxn, offset=offset, limit=limit
    )
