"""Autocomplete FDA manufacturers via the HC platform API."""

from __future__ import annotations

from hc_http.fda._cache_key import DEFAULT_CACHE_KEY
from hc_http.fda._versions_body import _versions_body
from hc_http.hc_request import hc_request_json
from model.fda_scrape_versions import FdaScrapeVersions


def run_autocomplete_fdalabel_manufacturer(
    manufacturer: str,
    *,
    versions: FdaScrapeVersions | None = None,
    cache_key: str = DEFAULT_CACHE_KEY,
) -> list[str]:
    """POST /fdalabels/search_manufacturer and return matching names."""
    data = hc_request_json(
        "POST",
        "/fdalabels/search_manufacturer",
        params={"manufacturer": manufacturer, "cache_key": cache_key},
        json_body=_versions_body(versions),
    )
    if not isinstance(data, list):
        raise RuntimeError(f"Unexpected HC API response type: {type(data).__name__}")
    return [str(item) for item in data]
