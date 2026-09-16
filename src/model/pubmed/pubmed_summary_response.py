"""PubMed esummary top-level response."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from model.pubmed.pubmed_summary_doc import PubmedSummaryDoc


class PubmedSummaryResponse(BaseModel):
    """NCBI esummary JSON with uids + per-PMID docs under result."""

    model_config = ConfigDict(extra="allow")

    uids: list[str] = Field(
        default_factory=list, description="PMID list present in this payload"
    )
    documents: dict[str, PubmedSummaryDoc] = Field(
        default_factory=dict,
        description="Map of PMID → summary document",
    )

    @model_validator(mode="before")
    @classmethod
    def _unwrap_result(cls, value: Any) -> Any:
        if not isinstance(value, dict):
            return value
        result = value.get("result")
        if not isinstance(result, dict):
            return value
        uids = [str(uid) for uid in result.get("uids", [])]
        documents: dict[str, Any] = {}
        for uid in uids:
            doc = result.get(uid)
            if isinstance(doc, dict):
                documents[uid] = doc
        return {"uids": uids, "documents": documents, **value}
