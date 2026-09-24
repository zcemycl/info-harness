"""LLM-as-judge score for an eval case."""

from __future__ import annotations

from pydantic import BaseModel, Field


class JudgeScore(BaseModel):
    """Structured judge output (1–5 scale)."""

    score: float = Field(ge=1, le=5, description="Overall quality 1–5")
    rationale: str = Field(description="Short justification")
    faithfulness: float | None = Field(default=None, ge=1, le=5)
    completeness: float | None = Field(default=None, ge=1, le=5)
    tool_use: float | None = Field(default=None, ge=1, le=5)
    passed: bool = Field(
        default=False,
        description="Filled by scorer from threshold; judge may omit",
    )
