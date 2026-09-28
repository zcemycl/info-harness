"""Read how many runs a user has taken in the open window."""

from __future__ import annotations

from tools.billing.billing_client import billing_client
from tools.billing.ensure_billing_tables import USAGE_TABLE
from tools.billing.usage_period import usage_period


def read_usage(user_id: str) -> tuple[int, str | None, str | None]:
    """Return ``(count, period_start, period_end)``. Missing storage counts as 0."""
    client = billing_client()
    if client is None:
        return 0, None, None
    period = usage_period(user_id, client)
    found = client.get_item(
        TableName=USAGE_TABLE,
        Key={"user_id": {"S": user_id}, "period": {"S": period.key}},
    )
    raw = found.get("Item", {}).get("count", {}).get("N", "0")
    return int(raw), period.start.isoformat(), period.end.isoformat()
