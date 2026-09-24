"""Tool: list conditions for a therapeutic area."""

from __future__ import annotations

from hc_http.therapeutic_area.get_condition_by_ta import (
    DEFAULT_TA,
    run_get_condition_by_ta,
)


def get_condition_by_ta(ta: str = DEFAULT_TA) -> list[str]:
    """List Level-1 conditions for a therapeutic area."""
    return run_get_condition_by_ta(ta)
