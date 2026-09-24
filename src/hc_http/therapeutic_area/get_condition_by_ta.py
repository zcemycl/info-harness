"""List Level-1 conditions for a therapeutic area (public HC API)."""

from __future__ import annotations

from hc_http.hc_request import hc_request_json

DEFAULT_TA = "Diseases of the Immune System"


def run_get_condition_by_ta(ta: str = DEFAULT_TA) -> list[str]:
    """GET /get_condition_by_ta and return Level-1 condition names."""
    data = hc_request_json(
        "GET",
        "/get_condition_by_ta",
        params={"ta": ta},
        auth=True,
    )
    if not isinstance(data, list):
        raise RuntimeError(f"Unexpected HC API response type: {type(data).__name__}")
    return [str(item) for item in data]
