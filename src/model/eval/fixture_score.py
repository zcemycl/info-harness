"""Deterministic fixture scoring result."""

from __future__ import annotations

from pydantic import BaseModel, Field


class FixtureCheck(BaseModel):
    """One named fixture assertion."""

    name: str
    ok: bool
    detail: str = ""


class FixtureScore(BaseModel):
    """Aggregate fixture pass/fail for one case run."""

    passed: bool
    checks: list[FixtureCheck] = Field(default_factory=list)
