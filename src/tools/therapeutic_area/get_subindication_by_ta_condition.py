"""Tool: list subindications for a TA + condition."""

from __future__ import annotations

from hc_http.therapeutic_area.get_subindication_by_ta_condition import (
    DEFAULT_CONDITION,
    DEFAULT_TA,
    run_get_subindication_by_ta_condition,
)


def get_subindication_by_ta_condition(
    ta: str = DEFAULT_TA,
    condition: str = DEFAULT_CONDITION,
) -> list[str]:
    """List Level-2 subindications for a therapeutic area and condition."""
    return run_get_subindication_by_ta_condition(ta, condition)
