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
    summary: str = Field(description="Full unit text for the evaluator (no truncation)")
    offset: int = Field(default=0, ge=0)
    next_offset: int | None = Field(
        default=None, description="Pagination cursor from the source page"
    )
