"""List Level-2 subindications for a TA + condition (public HC API)."""

from __future__ import annotations

from hc_http.hc_request import hc_request_json

DEFAULT_TA = "Diseases of the Immune System"
DEFAULT_CONDITION = "Vaccine"


def run_get_subindication_by_ta_condition(
    ta: str = DEFAULT_TA,
    condition: str = DEFAULT_CONDITION,
) -> list[str]:
    """GET /get_subindication_by_ta_condition and return Level-2 names."""
    data = hc_request_json(
        "GET",
        "/get_subindication_by_ta_condition",
        params={"ta": ta, "condition": condition},
        auth=True,
    )
    if not isinstance(data, list):
        raise RuntimeError(f"Unexpected HC API response type: {type(data).__name__}")
    return [str(item) for item in data]
