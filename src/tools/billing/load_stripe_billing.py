"""Build the signed-in user's Stripe allowance."""

from __future__ import annotations

from datetime import UTC, datetime

from model.billing.billing_config import BillingConfig
from model.billing.billing_status import BillingStatus
from tools.billing.read_entitlement import read_entitlement
from tools.billing.read_usage import read_usage


def load_stripe_billing(user_id: str) -> BillingStatus:
    """Return free or pro usage for ``BILLING_MODE=stripe``."""
    config = BillingConfig.from_env()
    entitlement = read_entitlement(user_id)
    used, period_start, period_end = read_usage(user_id)
    pro = entitlement.grants_pro(datetime.now(UTC))
    limit = config.pro_research_runs if pro else config.free_research_runs
    return BillingStatus(
        mode="stripe",
        plan="pro" if pro else "free",
        status=entitlement.status,
        runs_used=used,
        runs_limit=limit,
        period_start=period_start,
        period_end=period_end,
    )
