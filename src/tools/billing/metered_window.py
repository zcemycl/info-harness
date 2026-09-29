"""Choose the free anniversary window or the Stripe billing period."""

from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any

from model.billing.usage_period import UsagePeriod
from tools.billing.read_entitlement import read_entitlement
from tools.billing.usage_period import usage_period


def metered_window(user_id: str, client: Any, today: date | None = None) -> UsagePeriod:
    """Return the usage key for this message.

    An active or trialing subscription uses ``pro#{period_start}``. Everyone
    else stays on the free anniversary window.
    """
    now = datetime.now(UTC)
    entitlement = read_entitlement(user_id, client)
    start = entitlement.current_period_start
    end = entitlement.current_period_end
    if entitlement.grants_pro(now) and start is not None and end is not None:
        return UsagePeriod(
            start=datetime.fromtimestamp(start, UTC).date(),
            end=datetime.fromtimestamp(end, UTC).date(),
            key=f"pro#{start}",
        )
    return usage_period(user_id, client, today)
