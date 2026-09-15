"""Fetch FDA labels for an exact manufacturer via the HC platform API."""

from __future__ import annotations

from typing import Any

from hc_http.fda._versions_body import _versions_body
from hc_http.hc_request import hc_request_json
from model.fda_scrape_versions import FdaScrapeVersions


def run_search_fdalabel_by_manufacturer(
    manufacturer: str,
    *,
    versions: FdaScrapeVersions | None = None,
) -> dict[str, Any]:
    """POST /fdalabels/search_by_manufacturer and return manufacturer payload."""
    data = hc_request_json(
        "POST",
        "/fdalabels/search_by_manufacturer",
        params={"manufacturer": manufacturer},
        json_body=_versions_body(versions),
    )
    if not isinstance(data, dict):
        raise RuntimeError(f"Unexpected HC API response type: {type(data).__name__}")
    return data
