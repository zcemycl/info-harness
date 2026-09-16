"""Tool: search FDA labels by therapeutic area description."""

from __future__ import annotations

from hc_http.fda.search_by_therapeutic_area import (
    DEFAULT_SORT_BY,
    run_search_fdalabel_by_therapeutic_area,
)
from model.fda.fda_label import FdaLabel
from model.fda_scrape_versions import FdaScrapeVersions


def search_fdalabel_by_therapeutic_area(
    ta_description: str,
    *,
    versions: FdaScrapeVersions | None = None,
    maxn: int = 30,
    offset: int = 0,
    limit: int = 10,
    sort_by: str = DEFAULT_SORT_BY,
) -> list[FdaLabel]:
    """Search FDA labels by therapeutic area description."""
    return run_search_fdalabel_by_therapeutic_area(
        ta_description,
        versions=versions,
        maxn=maxn,
        offset=offset,
        limit=limit,
        sort_by=sort_by,
    )
