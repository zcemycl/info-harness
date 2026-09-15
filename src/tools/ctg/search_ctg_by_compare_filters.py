"""Tool: search CTG studies by compare filters."""

from __future__ import annotations

from typing import Any

from hc_http.ctg.search_by_compare_filters import (
    DEFAULT_CACHE_KEY,
    run_search_ctg_by_compare_filters,
)
from model.advanced_filters import AdvancedFilterPayload
from model.fda_scrape_versions import FdaScrapeVersions
from model.refine_filters import RefineFilters


def search_ctg_by_compare_filters(
    *,
    advanced_filter: AdvancedFilterPayload | None = None,
    refined_filters: RefineFilters | None = None,
    versions: FdaScrapeVersions | None = None,
    limit: int = 10,
    offset: int = 0,
    cache_key: str = DEFAULT_CACHE_KEY,
) -> list[dict[str, Any]]:
    """Search CTG studies with advanced + refine compare filters."""
    return run_search_ctg_by_compare_filters(
        advanced_filter=advanced_filter,
        refined_filters=refined_filters,
        versions=versions,
        limit=limit,
        offset=offset,
        cache_key=cache_key,
    )
