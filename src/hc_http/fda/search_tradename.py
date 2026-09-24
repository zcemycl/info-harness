"""Autocomplete FDA tradenames via the HC platform API."""

from __future__ import annotations

from hc_http.fda._cache_key import DEFAULT_CACHE_KEY
from hc_http.fda._versions_body import _versions_body
from hc_http.hc_request import hc_request_json
from model.fda_scrape_versions import FdaScrapeVersions


def run_autocomplete_fdalabel_tradename(
    tradename: str,
    *,
    versions: FdaScrapeVersions | None = None,
    cache_key: str = DEFAULT_CACHE_KEY,
) -> list[str]:
    """POST /fdalabels/search_tradename and return matching tradename strings."""
    data = hc_request_json(
        "POST",
        "/fdalabels/search_tradename",
        params={"tradename": tradename, "cache_key": cache_key},
        json_body=_versions_body(versions),
    )
    if not isinstance(data, list):
        raise RuntimeError(f"Unexpected HC API response type: {type(data).__name__}")
    return [str(item) for item in data]
