"""Compact writer note stored in the CTG specialist evidence ledger."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from model.ctg.ctg_attr_name import CtgAttrName
from model.ctg.ctg_worker_plan import CtgWorkerName


class CtgEvidenceNote(BaseModel):
    """One compressed evidence row from a CTG worker result."""

    worker: CtgWorkerName
    query: str
    attr: CtgAttrName | None = Field(
        default=None, description="Section attr when worker=nctid or fetch"
    )
    nctid: str | None = Field(default=None, description="NCT id when known")
    setid: UUID | str | None = Field(
        default=None, description="Linked FDA setid when present"
    )
    names: list[str] = Field(
        default_factory=list,
        description=(
            "Condition name hits when worker=condition; "
            "alias expansions when worker=resolve_trial; "
            "PMIDs when attr=references"
        ),
    )
    summary: str = Field(description="Short text excerpt for the evaluator")
    offset: int = Field(default=0, ge=0)
    next_offset: int | None = Field(
        default=None, description="Pagination cursor from the source page"
    )
    both_sides: bool | None = Field(
        default=None, description="LIKE mode when worker=condition"
    )
