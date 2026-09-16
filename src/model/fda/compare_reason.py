"""Reason entry attached to FDA compare-filter hits."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class CompareReason(BaseModel):
    """Explainability metric for why a compare-filter row matched."""

    model_config = ConfigDict(extra="allow")

    metric: str | None = Field(
        default=None, description="Internal metric key, e.g. MATCH_LEVEL_ind"
    )
    value: Any = Field(
        default=None, description="Metric value (score, overlap count, etc.)"
    )
    type: str | None = Field(
        default=None,
        description="Human-readable reason type, e.g. Indication Score",
    )
