"""Return a reserved research run when starting research fails."""

from __future__ import annotations

from botocore.exceptions import ClientError

from tools.billing.billing_client import billing_client
from tools.billing.table_names import billing_table_names
from tools.billing.usage_period import usage_period


def release_run(user_id: str) -> None:
    """Decrement the open window when a consumed run never starts."""
    client = billing_client()
    period = usage_period(user_id, client)
    usage = billing_table_names()[1]
    try:
        client.update_item(
            TableName=usage,
            Key={"user_id": {"S": user_id}, "period": {"S": period.key}},
            UpdateExpression="SET #c = #c - :one",
            ConditionExpression="attribute_exists(#c) AND #c > :zero",
            ExpressionAttributeNames={"#c": "count"},
            ExpressionAttributeValues={":one": {"N": "1"}, ":zero": {"N": "0"}},
        )
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code")
        if code != "ConditionalCheckFailedException":
            raise
