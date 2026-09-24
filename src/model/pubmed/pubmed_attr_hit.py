"""Slim PubMed hit carrying one projected MEDLINE section value."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from model.pubmed.pubmed_attr_name import PubmedAttrName


class PubmedAttrHit(BaseModel):
    """Fetch hit: pmid + one fixed section payload."""

    pmid: str = Field(description="PubMed identifier")
    attr: PubmedAttrName = Field(description="Which MEDLINE section this value is")
    value: Any = Field(description="Projected section value")
