"""Compare adverse-effects tables across FDA label setids."""

from __future__ import annotations

from hc_http.fda._versions_body import _versions_body
from hc_http.hc_request import hc_request_json
from model.compare_adverse_effects_item import CompareAdverseEffectsItem
from model.fda.compare_adverse_effects_response import (
    CompareAdverseEffectsResponse,
)
from model.fda_scrape_versions import FdaScrapeVersions
from model.parse_model import parse_model


def run_compare_fdalabel_adverse_effects(
    setids: list[str],
    *,
    versions: FdaScrapeVersions | None = None,
) -> CompareAdverseEffectsResponse:
    """POST /fdalabels/compare/adverse-effects and return AE matrices."""
    data = hc_request_json(
        "POST",
        "/fdalabels/compare/adverse-effects",
        json_body={
            "item": CompareAdverseEffectsItem(setids=setids).model_dump(),
            "versions": _versions_body(versions),
        },
        timeout=120.0,
    )
    return parse_model(CompareAdverseEffectsResponse, data)
