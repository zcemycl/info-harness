"""Therapeutic area node attached to an FDA label."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TherapeuticArea(BaseModel):
    """ICD/TA taxonomy node (ltree path serialized as a dotted string)."""

    model_config = ConfigDict(extra="allow")

    id: UUID = Field(description="Therapeutic area UUID")
    name: str = Field(description="Human-readable therapeutic area name")
    path: str = Field(
        description="Ltree path as dotted string, e.g. neoplasms.malignant_..."
    )
