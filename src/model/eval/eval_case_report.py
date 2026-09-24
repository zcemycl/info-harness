"""Per-case eval report combining fixtures and LLM judge."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from model.eval.eval_layer import EvalLayer
from model.eval.fixture_score import FixtureScore
from model.eval.judge_score import JudgeScore


class EvalCaseReport(BaseModel):
    """Full report for one eval case execution."""

    case_id: str
    layer: EvalLayer
    brief: str
    passed: bool
    fixtures: FixtureScore
    judge: JudgeScore | None = None
    run_id: str | None = None
    answer_preview: str = ""
    extras: dict[str, Any] = Field(default_factory=dict)
