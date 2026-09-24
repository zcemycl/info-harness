"""Manufacturer aggregate returned by search_by_manufacturer."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from model.fda.company import CompanyBase
from model.fda.fda_label_ref import FdaLabelRef


class Manufacturer(BaseModel):
    """Exact-manufacturer search result with linked companies and labels."""

    model_config = ConfigDict(extra="allow")

    name: str = Field(description="Exact manufacturer name")
    companies: list[CompanyBase] = Field(
        default_factory=list, description="Companies under this manufacturer"
    )
    fdalabels: list[FdaLabelRef] = Field(
        default_factory=list, description="FDA labels for this manufacturer"
    )
