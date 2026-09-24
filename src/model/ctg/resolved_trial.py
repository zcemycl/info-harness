"""Result of resolving a study name / protocol id to an NCT (or not)."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class ResolvedTrialStatus(StrEnum):
    """Whether an NCT was found for the query."""

    RESOLVED = "resolved"
    UNRESOLVED = "unresolved"


class ResolvedTrial(BaseModel):
    """API-first resolution pack for a study mention."""

    query: str = Field(description="Original query string")
    status: ResolvedTrialStatus
    nctid: str | None = Field(default=None, description="Primary NCT when resolved")
    ctg_url: str | None = Field(default=None, description="Public CT.gov study URL")
    brief_title: str | None = None
    official_title: str | None = None
    acronym: str | None = None
    overall_status: str | None = None
    sources: list[str] = Field(
        default_factory=list,
        description="Resolution steps that contributed (e.g. ctgov_id, pubmed)",
    )
    pmids: list[str] = Field(
        default_factory=list,
        description="PubMed IDs consulted when PubMed was used",
    )
    aliases_tried: list[str] = Field(
        default_factory=list,
        description="Alias expansions attempted for this query",
    )
    candidate_nctids: list[str] = Field(
        default_factory=list,
        description="All NCT ids found before picking the primary",
    )
