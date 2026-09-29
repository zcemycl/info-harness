"""Billing mode and run caps loaded from the environment."""

from __future__ import annotations

import os
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field

BillingMode = Literal["open", "table", "stripe"]


class BillingConfig(BaseModel):
    """Backend switch for unrestricted chat, a free cap, or Stripe Pro."""

    mode: BillingMode
    free_research_runs: int | None = Field(default=None, ge=1)
    pro_research_runs: int | None = Field(default=None, ge=1)
    stripe_secret_key: str = ""
    stripe_price_id: str = ""
    stripe_webhook_secret: str = ""
    app_public_url: str = ""

    @classmethod
    def from_env(cls) -> BillingConfig:
        """Load ``BILLING_MODE`` and the caps that mode requires."""
        load_dotenv()
        mode = os.getenv("BILLING_MODE", "open").strip().lower()
        if mode not in ("open", "table", "stripe"):
            raise ValueError("BILLING_MODE must be open, table, or stripe")
        if mode == "open":
            return cls(mode="open")
        free = _positive("FREE_RESEARCH_RUNS")
        if mode == "table":
            return cls(mode="table", free_research_runs=free)
        return cls(
            mode="stripe",
            free_research_runs=free,
            pro_research_runs=_positive("PRO_RESEARCH_RUNS"),
            stripe_secret_key=os.getenv("STRIPE_SECRET_KEY", "").strip(),
            stripe_price_id=os.getenv("STRIPE_PRICE_ID", "").strip(),
            stripe_webhook_secret=os.getenv("STRIPE_WEBHOOK_SECRET", "").strip(),
            app_public_url=os.getenv("APP_PUBLIC_URL", "").strip().rstrip("/"),
        )

    def require_stripe(self) -> None:
        """Fail when Checkout, the portal, or the webhook cannot call Stripe."""
        missing = [
            name
            for name, value in (
                ("STRIPE_SECRET_KEY", self.stripe_secret_key),
                ("STRIPE_PRICE_ID", self.stripe_price_id),
                ("STRIPE_WEBHOOK_SECRET", self.stripe_webhook_secret),
                ("APP_PUBLIC_URL", self.app_public_url),
            )
            if not value
        ]
        if missing:
            raise ValueError("missing " + ", ".join(missing))


def _positive(name: str) -> int:
    raw = os.getenv(name, "").strip()
    if not raw:
        raise ValueError(f"{name} is required")
    try:
        runs = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be a positive integer") from exc
    if runs < 1:
        raise ValueError(f"{name} must be a positive integer")
    return runs
