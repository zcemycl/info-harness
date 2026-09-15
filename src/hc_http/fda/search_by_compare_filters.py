"""Search FDA labels by advanced compare filters."""

from __future__ import annotations

from typing import Any

from hc_http.compare_filters_body import compare_filters_body
from hc_http.hc_request import hc_request_json
from model.advanced_filters import AdvancedFilterPayload
from model.fda_scrape_versions import FdaScrapeVersions
from model.refine_filters import RefineFilters

DEFAULT_CACHE_KEY = "2026-03-26d"


def run_search_fdalabel_by_compare_filters(
    *,
    advanced_filter: AdvancedFilterPayload | None = None,
    refined_filters: RefineFilters | None = None,
    versions: FdaScrapeVersions | None = None,
    limit: int = 10,
    offset: int = 0,
    embedding_threshold: float = 0.6,
    cache_key: str = DEFAULT_CACHE_KEY,
) -> list[dict[str, Any]]:
    """POST /fdalabels/search_by_compare_filters and return row dicts."""
    data = hc_request_json(
        "POST",
        "/fdalabels/search_by_compare_filters",
        params={
            "limit": limit,
            "offset": offset,
            "embedding_threshold": embedding_threshold,
            "cache_key": cache_key,
        },
        json_body=compare_filters_body(
            advanced_filter=advanced_filter,
            versions=versions,
            refined_filters=refined_filters,
            include_refined=True,
        ),
        timeout=120.0,
    )
    if not isinstance(data, list):
        raise RuntimeError(f"Unexpected HC API response type: {type(data).__name__}")
    return data
