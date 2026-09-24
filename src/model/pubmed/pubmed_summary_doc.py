"""PubMed esummary document entry."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class PubmedSummaryDoc(BaseModel):
    """One PubMed article summary from esummary.fcgi."""

    model_config = ConfigDict(extra="allow")

    uid: str | None = Field(default=None, description="PubMed UID / PMID")
    title: str | None = Field(default=None, description="Article title")
    authors: list[Any] | None = Field(
        default=None, description="Author list as returned by NCBI"
    )
    source: str | None = Field(default=None, description="Journal / source name")
    pubdate: str | None = Field(default=None, description="Publication date string")
    epubdate: str | None = Field(default=None, description="Electronic pub date")
    doi: str | None = Field(default=None, description="DOI when present")
    sortpubdate: str | None = Field(
        default=None, description="Sortable publication date"
    )
