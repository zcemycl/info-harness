"""CTG outcome measure nested under a trial outcome."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class CtgMeasure(BaseModel):
    """Single outcome measure (title + JSON data blob)."""

    model_config = ConfigDict(extra="allow")

    title: str | None = Field(default=None, description="Measure title")
    data: Any = Field(default=None, description="Raw measure data JSON")
