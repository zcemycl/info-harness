"""Slim FDA label hit carrying one projected attribute value."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from model.fda.fda_attr_name import FdaAttrName


class FdaLabelAttrHit(BaseModel):
    """Paginated search hit: ids + one fixed attr payload."""

    id: int = Field(description="Internal FDA label row id")
    setid: UUID = Field(description="SPL setid UUID")
    tradename: str = Field(description="Drug trade name")
    attr: FdaAttrName = Field(description="Which FdaLabel field this value is")
    value: Any = Field(description="Projected attribute value (embeddings stripped)")
