"""Search FDA labels by setid via the HC platform API."""

from __future__ import annotations

from typing import Any

from hc_http.fda._versions_body import _versions_body
from hc_http.hc_request import hc_request_json
from model.fda_scrape_versions import FdaScrapeVersions


def run_search_fdalabel_by_id(
    setids: list[str],
    *,
    versions: FdaScrapeVersions | None = None,
    maxn: int = 30,
    offset: int = 0,
    limit: int = 10,
) -> list[dict[str, Any]]:
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
    if not isinstance(data, list):
        raise RuntimeError(f"Unexpected HC API response type: {type(data).__name__}")
    return data
