"""ICD TA worker search plan (prefix or both-sides LIKE)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class IcdWorkerPlan(BaseModel):
    """One search_therapeutic_area invocation for the executor."""

    q: str = Field(description="Therapeutic area query string")
    both_sides: bool = Field(
        default=False,
        description=(
            "false → SQL LIKE q% (prefix only); "
            "true → SQL LIKE %q% (substring either side)"
        ),
    )
