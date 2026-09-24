"""Planner output: PubMed id-sections worker tasks."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field, model_validator

from model.pubmed.pubmed_attr_name import PubmedAttrName


class PubmedWorkerName(StrEnum):
    """Fixed PubMed workers the specialist may dispatch."""

    ID = "id"


class PubmedWorkerPlan(BaseModel):
    """One executor task for pubmed_id_sections."""

    worker: PubmedWorkerName = Field(
        description="Always 'id': fetch MEDLINE sections by PMID."
    )
    query: str = Field(description="PubMed PMID digits (e.g. 25712454).")
    attrs: list[PubmedAttrName] = Field(
        description=(
            "MEDLINE sections to return (min 1). Prefer abstract (+ citation) "
            "when present; if abstract is empty, use citation, mesh, "
            "keywords, chemicals, publication_types, secondary_ids."
        ),
    )
    offset: int = Field(default=0, ge=0, description="Pagination offset")
    limit: int = Field(
        default=20,
        ge=1,
        le=50,
        description="Page size over expanded section units",
    )

    @model_validator(mode="after")
    def _require_attrs_and_pmid(self) -> PubmedWorkerPlan:
        if self.worker is PubmedWorkerName.ID and not self.attrs:
            raise ValueError("worker=id requires at least one attr")
        pmid = self.query.strip()
        if not pmid.isdigit():
            raise ValueError(
                f"worker=id query must be a numeric PMID, got {self.query!r}"
            )
        return self
