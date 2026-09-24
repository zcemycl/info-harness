"""One table placeholder reference extracted from FDA section prose."""

from __future__ import annotations

from pydantic import BaseModel, Field


class FdaTablePlaceholderRef(BaseModel):
    """Link from section prose to a companion FdaLabelTable."""

    placeholder_index: int = Field(ge=0, description="Index in <tableplaceholder/>-N")
    table_number: int | None = Field(
        default=None, description="Table N from nearby prose when present"
    )
    context_snippet: str = Field(
        default="", description="Short text preceding the placeholder"
    )
