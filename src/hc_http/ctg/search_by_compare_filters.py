"""Search CTG studies by advanced compare filters."""

from __future__ import annotations

from hc_http.compare_filters_body import compare_filters_body
from hc_http.hc_request import hc_request_json
from model.advanced_filters import AdvancedFilterPayload
from model.ctg.ctg_compare_filter_row import CtgCompareFilterRow
from model.fda_scrape_versions import FdaScrapeVersions
from model.parse_model_list import parse_model_list
from model.refine_filters import RefineFilters

DEFAULT_CACHE_KEY = "2026-03-26c"


def run_search_ctg_by_compare_filters(
    *,
    advanced_filter: AdvancedFilterPayload | None = None,
    refined_filters: RefineFilters | None = None,
    versions: FdaScrapeVersions | None = None,
    limit: int = 10,
    offset: int = 0,
    cache_key: str = DEFAULT_CACHE_KEY,
) -> list[CtgCompareFilterRow]:
    """POST /ctg/search_by_compare_filters and return typed rows."""
    data = hc_request_json(
        "POST",
        "/ctg/search_by_compare_filters",
        params={"limit": limit, "offset": offset, "cache_key": cache_key},
        json_body=compare_filters_body(
            advanced_filter=advanced_filter,
            versions=versions,
            refined_filters=refined_filters,
            include_refined=True,
        ),
        timeout=120.0,
    )
    return parse_model_list(CtgCompareFilterRow, data)
