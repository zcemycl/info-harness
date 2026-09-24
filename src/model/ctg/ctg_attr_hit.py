"""Slim CTG study hit carrying one projected section value."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from model.ctg.ctg_attr_name import CtgAttrName


class CtgAttrHit(BaseModel):
    """Search hit: ids + one fixed section payload."""

    id: UUID | str | None = Field(default=None, description="CTG row UUID")
    setid: UUID | str | None = Field(
        default=None, description="Linked FDA setid when present"
    )
    nctid: str = Field(description="NCT identifier, e.g. NCT01234567")
    attr: CtgAttrName = Field(description="Which study section this value is")
    value: Any = Field(description="Projected section value")
