"""Projected ClinicalTrials.gov API v2 study fields."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CtgovStudyHit(BaseModel):
    """Slim study hit from CT.gov /studies."""

    nctid: str = Field(description="NCT identifier, e.g. NCT01234567")
    brief_title: str | None = Field(default=None)
    official_title: str | None = Field(default=None)
    acronym: str | None = Field(default=None)
    org_study_id: str | None = Field(
        default=None, description="Sponsor / org protocol id when present"
    )
    overall_status: str | None = Field(default=None)
    ctg_url: str = Field(description="Public study URL on ClinicalTrials.gov")
