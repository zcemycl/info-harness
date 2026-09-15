"""Autocomplete CTG condition names via the HC platform API."""

from __future__ import annotations

from hc_http.hc_request import hc_request_json


def run_search_ctg_condition(
    q: str,
    *,
    both_sides: bool = False,
) -> list[str]:
    """GET /ctg/search_condition and return matching condition names."""
    data = hc_request_json(
        "GET",
        "/ctg/search_condition",
        params={"q": q, "both_sides": both_sides},
    )
    if not isinstance(data, list):
        raise RuntimeError(f"Unexpected HC API response type: {type(data).__name__}")
    return [str(item) for item in data]
