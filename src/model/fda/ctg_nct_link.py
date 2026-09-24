"""NCT id + ClinicalTrials.gov study URL extracted from label text."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CtgNctLink(BaseModel):
    """Canonical NCT identifier with its public CTG study URL."""

    nctid: str = Field(description="Canonical NCT id, e.g. NCT01564784")
    ctg_url: str = Field(description="ClinicalTrials.gov study URL for this NCT id")
