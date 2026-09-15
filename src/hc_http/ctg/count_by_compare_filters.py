"""Count CTG studies matching advanced compare filters."""

from __future__ import annotations

from hc_http.compare_filters_body import compare_filters_body
from hc_http.hc_request import hc_request_json
from model.advanced_filters import AdvancedFilterPayload
from model.fda_scrape_versions import FdaScrapeVersions

DEFAULT_CACHE_KEY = "2026-03-26c"


def run_count_ctg_by_compare_filters(
    *,
    advanced_filter: AdvancedFilterPayload | None = None,
    versions: FdaScrapeVersions | None = None,
    cache_key: str = DEFAULT_CACHE_KEY,
) -> int:
    """POST /ctg/count_search_by_compare_filters and return count."""
    data = hc_request_json(
        "POST",
        "/ctg/count_search_by_compare_filters",
        params={"cache_key": cache_key},
        json_body=compare_filters_body(
            advanced_filter=advanced_filter,
            versions=versions,
            include_refined=False,
        ),
        timeout=120.0,
    )
    if isinstance(data, bool) or not isinstance(data, int):
        raise RuntimeError(f"Unexpected HC API response type: {type(data).__name__}")
    return int(data)
