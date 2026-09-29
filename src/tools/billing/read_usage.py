"""Read how many runs a user has taken in the open window."""

from __future__ import annotations

from tools.billing.billing_client import billing_client
from tools.billing.metered_window import metered_window
from tools.billing.table_names import billing_table_names


def read_usage(user_id: str) -> tuple[int, str | None, str | None]:
    """Return ``(count, period_start, period_end)``. A missing row counts as 0."""
    client = billing_client()
    period = metered_window(user_id, client)
    usage = billing_table_names()[1]
    found = client.get_item(
        TableName=usage,
        Key={"user_id": {"S": user_id}, "period": {"S": period.key}},
    )
    raw = found.get("Item", {}).get("count", {}).get("N", "0")
    return int(raw), period.start.isoformat(), period.end.isoformat()
