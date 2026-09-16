"""CTG outcome bundle nested under get_by_nctids rows."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from model.ctg.ctg_measure import CtgMeasure


class CtgOutcome(BaseModel):
    """Outcome group with arm groups, timeframe, and measures."""

    model_config = ConfigDict(extra="allow")

    title: str | None = Field(default=None, description="Outcome title")
    type: str | None = Field(
        default=None, description="Outcome measure type enum value"
    )
    arm_groups: Any = Field(default=None, description="Arm-group JSON for this outcome")
    timeFrame: str | None = Field(
        default=None, description="Outcome time frame description"
    )
    measures: list[CtgMeasure] = Field(
        default_factory=list, description="Measures under this outcome"
    )
