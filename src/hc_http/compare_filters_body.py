"""Build JSON body for FDA/CTG compare-filter posts."""

from __future__ import annotations

from typing import Any

from hc_http.fda._versions_body import _versions_body
from model.advanced_filters import AdvancedFilterPayload
from model.fda_scrape_versions import FdaScrapeVersions
from model.refine_filters import RefineFilters


def compare_filters_body(
    *,
    advanced_filter: AdvancedFilterPayload | None,
    versions: FdaScrapeVersions | None,
    refined_filters: RefineFilters | None = None,
    include_refined: bool = True,
) -> dict[str, Any]:
    """Embed advanced_filter / versions / optional refined_filters for FastAPI."""
    body: dict[str, Any] = {
        "advanced_filter": (advanced_filter or AdvancedFilterPayload()).model_dump(
            by_alias=True
        ),
        "versions": _versions_body(versions),
    }
    if include_refined:
        body["refined_filters"] = (refined_filters or RefineFilters()).model_dump()
    return body
