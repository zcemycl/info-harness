"""Tool: search FDA labels by compare filters."""

from __future__ import annotations

from typing import Any

from hc_http.fda.search_by_compare_filters import (
    DEFAULT_CACHE_KEY,
    run_search_fdalabel_by_compare_filters,
)
from model.advanced_filters import AdvancedFilterPayload
from model.fda_scrape_versions import FdaScrapeVersions
from model.refine_filters import RefineFilters


def search_fdalabel_by_compare_filters(
    *,
    advanced_filter: AdvancedFilterPayload | None = None,
    refined_filters: RefineFilters | None = None,
    versions: FdaScrapeVersions | None = None,
    limit: int = 10,
    offset: int = 0,
    embedding_threshold: float = 0.6,
    cache_key: str = DEFAULT_CACHE_KEY,
) -> list[dict[str, Any]]:
    """Search FDA labels with advanced + refine compare filters."""
    return run_search_fdalabel_by_compare_filters(
        advanced_filter=advanced_filter,
        refined_filters=refined_filters,
        versions=versions,
        limit=limit,
        offset=offset,
        embedding_threshold=embedding_threshold,
        cache_key=cache_key,
    )
