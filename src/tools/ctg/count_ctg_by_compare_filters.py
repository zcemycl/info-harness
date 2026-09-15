"""Tool: count CTG studies matching compare filters."""

from __future__ import annotations

from hc_http.ctg.count_by_compare_filters import (
    DEFAULT_CACHE_KEY,
    run_count_ctg_by_compare_filters,
)
from model.advanced_filters import AdvancedFilterPayload
from model.fda_scrape_versions import FdaScrapeVersions


def count_ctg_by_compare_filters(
    *,
    advanced_filter: AdvancedFilterPayload | None = None,
    versions: FdaScrapeVersions | None = None,
    cache_key: str = DEFAULT_CACHE_KEY,
) -> int:
    """Count CTG studies matching advanced compare filters."""
    return run_count_ctg_by_compare_filters(
        advanced_filter=advanced_filter,
        versions=versions,
        cache_key=cache_key,
    )
