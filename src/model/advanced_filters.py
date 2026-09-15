"""Advanced filter schemas for HC compare-filter endpoints."""

from __future__ import annotations

from typing import Literal, Union

from pydantic import AliasChoices, BaseModel, Field


class AdvancedFilterLeafCondition(BaseModel):
    """Single leaf filter condition."""

    field: str
    type: Literal["exact", "prefix", "trgm", "embedding", "tatree_search"]
    value: str | list[str]


class AdvancedFilterGroup(BaseModel):
    """AND/OR group of filter nodes."""

    op: Literal["AND", "OR"] = Field(
        validation_alias=AliasChoices("op", "ops"),
        serialization_alias="op",
    )
    conditions: list["AdvancedFilterNode"]


AdvancedFilterNode = Union[AdvancedFilterGroup, AdvancedFilterLeafCondition]


class AdvancedFilterPayload(BaseModel):
    """Top-level advanced filter wrapper."""

    filters: AdvancedFilterNode | None = None


AdvancedFilterGroup.model_rebuild()
AdvancedFilterPayload.model_rebuild()
