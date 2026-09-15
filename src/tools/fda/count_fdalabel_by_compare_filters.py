"""Tool: count FDA labels matching compare filters."""

from __future__ import annotations

from hc_http.fda.count_by_compare_filters import (
    DEFAULT_CACHE_KEY,
    run_count_fdalabel_by_compare_filters,
)
from model.advanced_filters import AdvancedFilterPayload
from model.fda_scrape_versions import FdaScrapeVersions


def count_fdalabel_by_compare_filters(
    *,
    advanced_filter: AdvancedFilterPayload | None = None,
    versions: FdaScrapeVersions | None = None,
    embedding_threshold: float = 0.6,
    cache_key: str = DEFAULT_CACHE_KEY,
) -> int:
    """Count FDA labels matching advanced compare filters."""
    return run_count_fdalabel_by_compare_filters(
        advanced_filter=advanced_filter,
        versions=versions,
        embedding_threshold=embedding_threshold,
        cache_key=cache_key,
    )
