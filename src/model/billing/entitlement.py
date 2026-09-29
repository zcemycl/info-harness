"""Stored Stripe subscription for one Cognito user."""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel


class Entitlement(BaseModel):
    """Subscription fields on the billing entitlements item."""

    customer_id: str | None = None
    subscription_id: str | None = None
    status: str | None = None
    price_id: str | None = None
    current_period_start: int | None = None
    current_period_end: int | None = None

    def grants_pro(self, now: datetime) -> bool:
        """True while status is paying and the Stripe period has not ended."""
        if self.status not in ("active", "trialing"):
            return False
        if self.current_period_end is None:
            return False
        return now < datetime.fromtimestamp(self.current_period_end, UTC)
