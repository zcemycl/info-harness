"""CTG compare-filter search row."""

from __future__ import annotations

from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CtgCompareFilterRow(BaseModel):
    """One CTG hit from POST /ctg/search_by_compare_filters."""

    model_config = ConfigDict(extra="allow")

    ctg_id: UUID | str | None = Field(default=None, description="CTG row UUID")
    fdalabel_id: int | None = Field(
        default=None, description="Linked FDA label id when present"
    )
    tradename: str | None = Field(default=None, description="Linked trade name")
    nctid: str | None = Field(default=None, description="NCT identifier")
    phases: list[str] | None = Field(default=None, description="Trial phases")
    std_ages: list[str] | None = Field(default=None, description="Standard age groups")
    conditions: list[str] | None = Field(default=None, description="Trial conditions")
    countries: list[str] | None = Field(default=None, description="Trial countries")
    metric: Any = Field(
        default=None, description="Link/match metric value when present"
    )
    match_type: Literal["INTERNAL", "EXTERNAL"] | str | None = Field(
        default=None, description="Whether the CTG match is internal or external"
    )
    hasResults: bool | None = Field(
        default=None, description="Whether the CTG study reports results"
    )
    rn: int | None = Field(default=None, description="Row number / rank")
