"""Search FDA labels by setid via the HC platform API."""

from __future__ import annotations

from hc_http.fda._versions_body import _versions_body
from hc_http.hc_request import hc_request_json
from model.fda.fda_label import FdaLabel
from model.fda_scrape_versions import FdaScrapeVersions
from model.parse_model_list import parse_model_list


def run_search_fdalabel_by_id(
    setids: list[str],
    *,
    versions: FdaScrapeVersions | None = None,
    maxn: int = 30,
    offset: int = 0,
    limit: int = 10,
) -> list[FdaLabel]:
    """POST /fdalabels/search_by_id and return matching FDA labels."""
    data = hc_request_json(
        "POST",
        "/fdalabels/search_by_id",
        params={
            "id": setids,
            "maxn": maxn,
            "offset": offset,
            "limit": limit,
        },
        json_body=_versions_body(versions),
    )
    return parse_model_list(FdaLabel, data)
