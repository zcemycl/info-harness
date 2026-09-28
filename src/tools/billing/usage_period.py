"""Resolve the free-plan usage key for a user."""

from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any

from botocore.exceptions import ClientError

from model.billing.usage_period import UsagePeriod
from tools.billing.ensure_billing_tables import ENTITLEMENTS_TABLE
from tools.billing.open_window import open_window


def usage_period(user_id: str, client: Any, today: date | None = None) -> UsagePeriod:
    """Return this user's open free window, creating the anchor on first sight."""
    current = today or datetime.now(UTC).date()
    anchor = _anchor(user_id, client, current)
    start, end = open_window(anchor, current)
    return UsagePeriod(start=start, end=end, key=f"free#{start.isoformat()}")


def _anchor(user_id: str, client: Any, today: date) -> date:
    key = {"cognito_sub": {"S": user_id}}
    found = client.get_item(TableName=ENTITLEMENTS_TABLE, Key=key)
    raw = found.get("Item", {}).get("free_anchor", {}).get("S")
    if raw:
        return date.fromisoformat(str(raw))
    try:
        client.put_item(
            TableName=ENTITLEMENTS_TABLE,
            Item={
                "cognito_sub": {"S": user_id},
                "free_anchor": {"S": today.isoformat()},
            },
            ConditionExpression="attribute_not_exists(cognito_sub)",
        )
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code")
        if code != "ConditionalCheckFailedException":
            raise
        found = client.get_item(TableName=ENTITLEMENTS_TABLE, Key=key)
        raw = found.get("Item", {}).get("free_anchor", {}).get("S")
        if raw:
            return date.fromisoformat(str(raw))
    return today
