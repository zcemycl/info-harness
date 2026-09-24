"""CTG study row from GET /ctg/get_by_nctids."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from model.ctg.ctg_outcome import CtgOutcome


class CtgByNctidRow(BaseModel):
    """ClinicalTrials.gov study payload projected by HC get_by_nctids."""

    model_config = ConfigDict(extra="allow")

    id: UUID | str | None = Field(default=None, description="CTG row UUID")
    setid: UUID | str | None = Field(
        default=None, description="Linked FDA setid when present"
    )
    nctid: str = Field(description="NCT identifier, e.g. NCT01234567")
    brief_title: str | None = Field(default=None, description="Brief title")
    official_title: str | None = Field(default=None, description="Official title")
    enrollment_no: int | None = Field(
        default=None, description="Enrollment count when known"
    )
    description: str | None = Field(default=None, description="Study description text")
    phases: list[str] | None = Field(default=None, description="Trial phase labels")
    arm_groups: Any = Field(default=None, description="Demographic arm-group JSON")
    eligibility_criteria: str | None = Field(
        default=None, description="Eligibility criteria text"
    )
    std_ages: list[str] | None = Field(
        default=None, description="Standard age-group enum values"
    )
    conditions: list[str] | None = Field(default=None, description="Condition names")
    countries: list[str] | None = Field(
        default=None, description="Country names from locations"
    )
    aes: Any = Field(default=None, description="Adverse-event measures_raw JSON")
    ae_arms: Any = Field(default=None, description="AE arm-group JSON")
    outcomes: list[CtgOutcome] = Field(
        default_factory=list, description="Normalized outcome bundles"
    )
