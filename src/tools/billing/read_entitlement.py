"""Read the Stripe fields stored for one Cognito user."""

from __future__ import annotations

from typing import Any

from model.billing.entitlement import Entitlement
from tools.billing.billing_client import billing_client
from tools.billing.table_names import billing_table_names


def read_entitlement(user_id: str, client: Any | None = None) -> Entitlement:
    """Return the entitlement. A missing item is an empty free user."""
    dynamo = billing_client() if client is None else client
    found = dynamo.get_item(
        TableName=billing_table_names()[0],
        Key={"cognito_sub": {"S": user_id}},
    )
    item = found.get("Item") or {}
    return Entitlement(
        customer_id=_text(item, "customer_id"),
        subscription_id=_text(item, "subscription_id"),
        status=_text(item, "status"),
        price_id=_text(item, "price_id"),
        current_period_start=_number(item, "current_period_start"),
        current_period_end=_number(item, "current_period_end"),
    )


def _text(item: dict[str, Any], name: str) -> str | None:
    raw = item.get(name, {}).get("S")
    return str(raw) if raw else None


def _number(item: dict[str, Any], name: str) -> int | None:
    raw = item.get(name, {}).get("N")
    return int(raw) if raw else None
