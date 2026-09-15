"""List available FDA scrape versions via the HC platform API."""

from __future__ import annotations

from hc_http.hc_request import hc_request_json


def run_get_fdalabel_scrape_versions() -> list[str]:
    """GET /fdalabels/get_scrape_version and return version strings."""
    data = hc_request_json("GET", "/fdalabels/get_scrape_version")
    if not isinstance(data, list):
        raise RuntimeError(f"Unexpected HC API response type: {type(data).__name__}")
    return [str(item) for item in data]
