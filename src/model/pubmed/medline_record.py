"""Parsed PubMed MEDLINE record (tag → values)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class MedlineRecord(BaseModel):
    """One MEDLINE citation as multi-valued tag map."""

    pmid: str = Field(description="PMID from the PMID tag")
    tags: dict[str, list[str]] = Field(
        default_factory=dict,
        description="Tag code → one or more field values (continuations joined)",
    )
