"""Fetch FDA label history by setid via the HC platform API."""

from __future__ import annotations

from typing import Any

from hc_http.fda._versions_body import _versions_body
from hc_http.hc_request import hc_request_json
from model.fda_scrape_versions import FdaScrapeVersions


def run_fdalabel_history_by_id(
    setid: str,
    *,
    versions: FdaScrapeVersions | None = None,
) -> dict[str, Any]:
    """POST /fdalabels/history/{id} and return label history."""
    data = hc_request_json(
        "POST",
        f"/fdalabels/history/{setid}",
        json_body=_versions_body(versions),
    )
    if not isinstance(data, dict):
        raise RuntimeError(f"Unexpected HC API response type: {type(data).__name__}")
    return data
