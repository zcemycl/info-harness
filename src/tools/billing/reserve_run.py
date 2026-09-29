"""Consume one research run when the billing mode meters usage."""

from __future__ import annotations

from datetime import UTC, datetime

from model.billing.billing_config import BillingConfig
from tools.billing.billing_client import billing_client
from tools.billing.consume_run import consume_run
from tools.billing.read_entitlement import read_entitlement


def reserve_run(user_id: str) -> bool:
    """Consume one run in ``table`` or ``stripe``. ``open`` consumes nothing."""
    config = BillingConfig.from_env()
    if config.mode == "open":
        return False
    consume_run(user_id, _limit(user_id, config))
    return True


def _limit(user_id: str, config: BillingConfig) -> int:
    free = config.free_research_runs
    if free is None:
        raise ValueError("FREE_RESEARCH_RUNS is required")
    if config.mode != "stripe":
        return free
    entitlement = read_entitlement(user_id, billing_client())
    if not entitlement.grants_pro(datetime.now(UTC)):
        return free
    pro = config.pro_research_runs
    if pro is None:
        raise ValueError("PRO_RESEARCH_RUNS is required")
    return pro
