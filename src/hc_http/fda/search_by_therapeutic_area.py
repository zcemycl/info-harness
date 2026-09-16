"""Search FDA labels by therapeutic area via the HC platform API."""

from __future__ import annotations

from hc_http.fda._versions_body import _versions_body
from hc_http.hc_request import hc_request_json
from model.fda.fda_label import FdaLabel
from model.fda_scrape_versions import FdaScrapeVersions
from model.parse_model_list import parse_model_list

DEFAULT_SORT_BY = "relevance"


def run_search_fdalabel_by_therapeutic_area(
    ta_description: str,
    *,
    versions: FdaScrapeVersions | None = None,
    maxn: int = 30,
    offset: int = 0,
    limit: int = 10,
    sort_by: str = DEFAULT_SORT_BY,
) -> list[FdaLabel]:
    """POST /fdalabels/search_by_therapeutic_area and return matching labels."""
    data = hc_request_json(
        "POST",
        "/fdalabels/search_by_therapeutic_area",
        params={
            "ta_description": ta_description,
            "maxn": maxn,
            "offset": offset,
            "limit": limit,
            "sort_by": sort_by,
        },
        json_body=_versions_body(versions),
    )
    return parse_model_list(FdaLabel, data)
