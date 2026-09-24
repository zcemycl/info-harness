"""Compact writer note for the PubMed specialist evidence ledger."""

from __future__ import annotations

from pydantic import BaseModel, Field

from model.pubmed.pubmed_attr_name import PubmedAttrName
from model.pubmed.pubmed_worker_plan import PubmedWorkerName


class PubmedEvidenceNote(BaseModel):
    """One compressed evidence row from a PubMed worker result."""

    worker: PubmedWorkerName
    query: str
    attr: PubmedAttrName | None = Field(
        default=None, description="Section attr when worker=id"
    )
    pmid: str | None = Field(default=None, description="PMID when known")
    names: list[str] = Field(
        default_factory=list,
        description="Secondary ids / NCT / DOI strings when attr=secondary_ids",
    )
    summary: str = Field(description="Capped text excerpt for the evaluator")
    artifact_path: str | None = Field(
        default=None, description="Diary path to full value when summary is capped"
    )
    total_chars: int | None = Field(
        default=None, description="Full value length before summary cap"
    )
    offset: int = Field(default=0, ge=0)
    next_offset: int | None = Field(
        default=None, description="Pagination cursor from the source page"
    )
