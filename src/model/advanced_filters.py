"""Advanced filter schemas for HC compare-filter endpoints."""

from __future__ import annotations

from typing import Literal, Union

from pydantic import AliasChoices, BaseModel, Field


class AdvancedFilterLeafCondition(BaseModel):
    """Single leaf filter condition for compare-filter search."""

    field: str = Field(
        description="Filter field name, e.g. tradename, indication, therapeutic_area"
    )
    type: Literal["exact", "prefix", "trgm", "embedding", "tatree_search"] = Field(
        description="Match strategy for this leaf"
    )
    value: str | list[str] = Field(
        description="Filter value or list of values for the leaf"
    )


class AdvancedFilterGroup(BaseModel):
    """AND/OR group of filter nodes."""

    op: Literal["AND", "OR"] = Field(
        description="Boolean operator for child conditions",
        validation_alias=AliasChoices("op", "ops"),
        serialization_alias="op",
    )
    conditions: list["AdvancedFilterNode"] = Field(
        description="Nested leaf or group conditions"
    )


AdvancedFilterNode = Union[AdvancedFilterGroup, AdvancedFilterLeafCondition]


class AdvancedFilterPayload(BaseModel):
    """Top-level advanced filter wrapper sent to compare-filter endpoints."""

    filters: AdvancedFilterNode | None = Field(
        default=None,
        description="Recursive filter tree; null means no advanced filter",
    )


AdvancedFilterGroup.model_rebuild()
AdvancedFilterPayload.model_rebuild()
