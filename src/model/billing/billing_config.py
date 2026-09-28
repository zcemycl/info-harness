"""Billing mode and free-run cap loaded from the environment."""

from __future__ import annotations

import os
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field

BillingMode = Literal["open", "table"]


class BillingConfig(BaseModel):
    """Backend switch for unrestricted chat or a shared free-run cap."""

    mode: BillingMode
    free_research_runs: int | None = Field(default=None, ge=1)

    @classmethod
    def from_env(cls) -> BillingConfig:
        """Load ``BILLING_MODE`` and, in table mode, ``FREE_RESEARCH_RUNS``."""
        load_dotenv()
        mode = os.getenv("BILLING_MODE", "open").strip().lower()
        if mode not in ("open", "table"):
            raise ValueError("BILLING_MODE must be open or table")
        if mode == "open":
            return cls(mode="open")
        raw = os.getenv("FREE_RESEARCH_RUNS", "").strip()
        if not raw:
            raise ValueError("FREE_RESEARCH_RUNS is required when BILLING_MODE=table")
        try:
            runs = int(raw)
        except ValueError as exc:
            raise ValueError("FREE_RESEARCH_RUNS must be a positive integer") from exc
        if runs < 1:
            raise ValueError("FREE_RESEARCH_RUNS must be a positive integer")
        return cls(mode="table", free_research_runs=runs)
