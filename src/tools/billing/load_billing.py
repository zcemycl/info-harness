"""Read the backend billing mode, cap, and runs already used."""

from __future__ import annotations

from model.billing.billing_config import BillingConfig
from model.billing.billing_status import BillingStatus
from tools.billing.load_stripe_billing import load_stripe_billing
from tools.billing.read_usage import read_usage


def load_billing(user_id: str) -> BillingStatus:
    """Return the shared cap. ``open`` has no limit. ``table`` and ``stripe`` do."""
    config = BillingConfig.from_env()
    if config.mode == "open":
        return BillingStatus(mode="open", plan="open")
    if config.mode == "stripe":
        return load_stripe_billing(user_id)
    used, period_start, period_end = read_usage(user_id)
    return BillingStatus(
        mode="table",
        plan="free",
        runs_used=used,
        runs_limit=config.free_research_runs,
        period_start=period_start,
        period_end=period_end,
    )
