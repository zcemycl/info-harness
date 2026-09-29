"""Take one research run from the open free window."""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError

from tools.billing.billing_client import billing_client
from tools.billing.ensure_billing_tables import USAGE_TABLE
from tools.billing.usage_period import usage_period


class RunQuotaExceeded(Exception):
    """The open window has already reached the free-run cap."""

    def __init__(self, used: int, limit: int, resets_on: str) -> None:
        super().__init__(f"used {used} of {limit}")
        self.used = used
        self.limit = limit
        self.resets_on = resets_on


def consume_run(user_id: str, limit: int, client: Any | None = None) -> int:
    """Add one to the open window. Raise when ``count`` is already at ``limit``."""
    dynamo = billing_client() if client is None else client
    period = usage_period(user_id, dynamo)
    key = {"user_id": {"S": user_id}, "period": {"S": period.key}}
    try:
        updated = dynamo.update_item(
            TableName=USAGE_TABLE,
            Key=key,
            UpdateExpression="SET #c = if_not_exists(#c, :zero) + :one",
            ConditionExpression="attribute_not_exists(#c) OR #c < :limit",
            ExpressionAttributeNames={"#c": "count"},
            ExpressionAttributeValues={
                ":zero": {"N": "0"},
                ":one": {"N": "1"},
                ":limit": {"N": str(limit)},
            },
            ReturnValues="UPDATED_NEW",
        )
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code")
        if code != "ConditionalCheckFailedException":
            raise
        raise RunQuotaExceeded(limit, limit, period.end.isoformat()) from exc
    return int(updated["Attributes"]["count"]["N"])
