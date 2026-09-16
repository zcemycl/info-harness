"""Fetch FDA labels for an exact manufacturer via the HC platform API."""

from __future__ import annotations

from hc_http.fda._versions_body import _versions_body
from hc_http.hc_request import hc_request_json
from model.fda.manufacturer import Manufacturer
from model.fda_scrape_versions import FdaScrapeVersions
from model.parse_model import parse_model


def run_search_fdalabel_by_manufacturer(
    manufacturer: str,
    *,
    versions: FdaScrapeVersions | None = None,
) -> Manufacturer:
    """POST /fdalabels/search_by_manufacturer and return manufacturer payload."""
    data = hc_request_json(
        "POST",
        "/fdalabels/search_by_manufacturer",
        params={"manufacturer": manufacturer},
        json_body=_versions_body(versions),
    )
    return parse_model(Manufacturer, data)
