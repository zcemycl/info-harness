"""Compact writer note stored in the specialist evidence ledger."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from model.research.worker_plan import FdaAttrName, FdaWorkerName


class EvidenceNote(BaseModel):
    """One compressed evidence row from a worker page hit."""

    worker: FdaWorkerName
    attr: FdaAttrName
    query: str
    label_id: int
    setid: UUID
    tradename: str
    summary: str = Field(description="Short text excerpt for the evaluator")
    offset: int = Field(ge=0)
    next_offset: int | None = Field(
        default=None, description="Pagination cursor from the source page"
    )
