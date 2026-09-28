"""Current user's research-run allowance."""

from __future__ import annotations

from pydantic import BaseModel, Field

from model.billing.billing_config import BillingMode


class BillingStatus(BaseModel):
    """Allowance the chat page shows for the signed-in user."""

    mode: BillingMode
    plan: str
    runs_used: int | None = None
    runs_limit: int | None = Field(default=None, ge=1)
    period_start: str | None = None
    period_end: str | None = None
