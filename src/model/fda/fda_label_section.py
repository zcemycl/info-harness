"""Shared FDA label section text block (hc-backend BaseSection)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class FdaLabelSection(BaseModel):
    """Label section row (indication, dosing, AE text, CT text, etc.)."""

    model_config = ConfigDict(extra="allow")

    id: int = Field(description="Section row id")
    tag: str = Field(description="Section XML/tag identifier")
    content: str | None = Field(
        default=None, description="Extracted section text content"
    )
    embedding: list[float] | None = Field(
        default=None, description="Optional embedding vector; often omitted"
    )
    version: str = Field(description="Section scrape/cache version pin")
