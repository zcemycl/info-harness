"""Compare adverse-effects tables across FDA label setids."""

from __future__ import annotations

from typing import Any

from hc_http.fda._versions_body import _versions_body
from hc_http.hc_request import hc_request_json
from model.compare_adverse_effects_item import CompareAdverseEffectsItem
from model.fda_scrape_versions import FdaScrapeVersions


def run_compare_fdalabel_adverse_effects(
    setids: list[str],
    *,
    versions: FdaScrapeVersions | None = None,
) -> dict[str, Any]:
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
    if not isinstance(data, dict):
        raise RuntimeError(f"Unexpected HC API response type: {type(data).__name__}")
    return data
