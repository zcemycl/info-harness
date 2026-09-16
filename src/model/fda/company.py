"""Company summary nested under FDA labels / manufacturers."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class CompanyBase(BaseModel):
    """Company linked to an FDA label or manufacturer."""

    model_config = ConfigDict(extra="allow")

    name: str = Field(description="Company legal/display name")
    ticker: str = Field(description="Stock ticker symbol when known")
    sector: str = Field(description="Industry sector label")
    website: str = Field(description="Company website URL")
