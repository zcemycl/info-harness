"""Write subscription fields without moving the free-plan anchor."""

from __future__ import annotations

from typing import Any

from model.billing.entitlement import Entitlement
from tools.billing.billing_client import billing_client
from tools.billing.table_names import billing_table_names

_TEXT = ("customer_id", "subscription_id", "status", "price_id")
_NUMBERS = ("current_period_start", "current_period_end")


def save_entitlement(
    user_id: str,
    entitlement: Entitlement,
    client: Any | None = None,
) -> None:
    """Upsert the subscription columns that are set. ``free_anchor`` stays."""
    fields = entitlement.model_dump(exclude_none=True)
    names: dict[str, str] = {}
    values: dict[str, dict[str, str]] = {}
    parts: list[str] = []
    for name in _TEXT:
        if name not in fields:
            continue
        token = f"#{name}"
        names[token] = name
        values[f":{name}"] = {"S": str(fields[name])}
        parts.append(f"{token} = :{name}")
    for name in _NUMBERS:
        if name not in fields:
            continue
        token = f"#{name}"
        names[token] = name
        values[f":{name}"] = {"N": str(fields[name])}
        parts.append(f"{token} = :{name}")
    if not parts:
        return
    dynamo = billing_client() if client is None else client
    dynamo.update_item(
        TableName=billing_table_names()[0],
        Key={"cognito_sub": {"S": user_id}},
        UpdateExpression="SET " + ", ".join(parts),
        ExpressionAttributeNames=names,
        ExpressionAttributeValues=values,
    )
