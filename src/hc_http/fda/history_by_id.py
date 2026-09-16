"""Fetch FDA label history by setid via the HC platform API."""

from __future__ import annotations

from hc_http.fda._versions_body import _versions_body
from hc_http.hc_request import hc_request_json
from model.fda.fda_label_history import FdaLabelHistory
from model.fda_scrape_versions import FdaScrapeVersions
from model.parse_model import parse_model


def run_fdalabel_history_by_id(
    setid: str,
    *,
    versions: FdaScrapeVersions | None = None,
) -> FdaLabelHistory:
    """POST /fdalabels/history/{id} and return label history."""
    data = hc_request_json(
        "POST",
        f"/fdalabels/history/{setid}",
        json_body=_versions_body(versions),
    )
    return parse_model(FdaLabelHistory, data)
