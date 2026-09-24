"""FDA compare-filter search row (not a full FdaLabel)."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from model.fda.compare_reason import CompareReason


class FdaCompareFilterRow(BaseModel):
    """One FDA hit from POST /fdalabels/search_by_compare_filters."""

    model_config = ConfigDict(extra="allow")

    tradename_lc: str | None = Field(
        default=None, description="Lowercased trade name used for grouping"
    )
    setid: UUID | str | None = Field(default=None, description="SPL setid")
    id: int | None = Field(default=None, description="FDA label row id")
    indication: str | None = Field(
        default=None, description="Indication text for the hit"
    )
    version: str | None = Field(default=None, description="Label scrape version")
    phases: list[str] | None = Field(default=None, description="Associated CTG phases")
    conditions: list[str] | None = Field(
        default=None, description="Associated CTG conditions"
    )
    countries: list[str] | None = Field(
        default=None, description="Associated trial countries"
    )
    std_ages: list[str] | None = Field(default=None, description="Standard age groups")
    clinical_pharmacology: str | None = Field(
        default=None, description="Clinical pharmacology excerpt"
    )
    dosing: str | None = Field(default=None, description="Dosing excerpt")
    moa: str | None = Field(default=None, description="Mechanism of action excerpt")
    treatment_line: str | None = Field(
        default=None, description="Treatment line when available"
    )
    manufacturers: list[Any] | None = Field(
        default=None, description="Manufacturer aggregate payload"
    )
    therapeutic_area: str | None = Field(
        default=None, description="Primary therapeutic area path/name"
    )
    therapeutic_area_id: str | UUID | None = Field(
        default=None, description="Primary therapeutic area id"
    )
    reasons: list[CompareReason] | None = Field(
        default=None, description="Match explainability reasons"
    )
    clinical_trials: list[Any] | None = Field(
        default=None, description="Reserved CTG nest; often empty today"
    )
    rn: int | None = Field(default=None, description="Row number / rank")
