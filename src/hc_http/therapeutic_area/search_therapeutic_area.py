"""Autocomplete therapeutic area names via the HC ICD API."""

from __future__ import annotations

from hc_http.hc_request import hc_request_json


def run_search_therapeutic_area(
    q: str,
    *,
    both_sides: bool = False,
) -> list[str]:
    """GET /icd/search_therapeutic_area and return matching TA names."""
    data = hc_request_json(
        "GET",
        "/icd/search_therapeutic_area",
        params={"q": q, "both_sides": both_sides},
    )
    if not isinstance(data, list):
        raise RuntimeError(f"Unexpected HC API response type: {type(data).__name__}")
    return [str(item) for item in data]
