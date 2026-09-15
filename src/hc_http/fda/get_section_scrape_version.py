"""List section scrape versions for an FDA label parent version."""

from __future__ import annotations

from typing import Any

from hc_http.hc_request import hc_request_json
from model.fda_scrape_versions import DEFAULT_SCRAPE_VERSION


def run_get_fdalabel_section_scrape_versions(
    version: str = DEFAULT_SCRAPE_VERSION,
) -> dict[str, Any]:
    """GET /fdalabels/get_section_scrape_version for a parent scrape version."""
    data = hc_request_json(
        "GET",
        "/fdalabels/get_section_scrape_version",
        params={"version": version},
    )
    if not isinstance(data, dict):
        raise RuntimeError(f"Unexpected HC API response type: {type(data).__name__}")
    return data
