"""PubMed esearch result from NCBI E-utilities."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class PubmedEsearchResult(BaseModel):
    """Inner esearchresult object from esearch.fcgi."""

    model_config = ConfigDict(extra="allow")

    count: str | int | None = Field(
        default=None, description="Total matching PubMed IDs"
    )
    retmax: str | int | None = Field(
        default=None, description="Number of IDs returned in this page"
    )
    retstart: str | int | None = Field(
        default=None, description="Offset into the result set"
    )
    idlist: list[str] = Field(
        default_factory=list, description="PubMed IDs (PMIDs) for this page"
    )
    querytranslation: str | None = Field(
        default=None, description="Translated query string from NCBI"
    )


class PubmedSearchResponse(BaseModel):
    """Top-level NCBI esearch JSON payload."""

    model_config = ConfigDict(extra="allow")

    esearchresult: PubmedEsearchResult = Field(description="Parsed esearch result body")
