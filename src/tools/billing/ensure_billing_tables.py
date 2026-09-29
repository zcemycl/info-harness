"""Create the local billing tables when DynamoDB Local is configured."""

from __future__ import annotations

import os
from typing import Any

from botocore.exceptions import ClientError

from tools.billing.billing_client import billing_client
from tools.billing.table_names import billing_table_names


def ensure_billing_tables(client: Any | None = None) -> None:
    """Create both billing tables if ``DYNAMODB_ENDPOINT_URL`` is set.

    ``open`` mode still creates them so switching to ``table`` does not need a
    second bootstrap. A missing endpoint leaves AWS tables to the deploy.
    """
    endpoint = os.getenv("DYNAMODB_ENDPOINT_URL", "").strip()
    if not endpoint:
        return
    dynamo = client or billing_client()
    if dynamo is None:
        return
    entitlements, usage = billing_table_names()
    _create_if_missing(
        dynamo,
        entitlements,
        [{"AttributeName": "cognito_sub", "AttributeType": "S"}],
        [{"AttributeName": "cognito_sub", "KeyType": "HASH"}],
    )
    _create_if_missing(
        dynamo,
        usage,
        [
            {"AttributeName": "user_id", "AttributeType": "S"},
            {"AttributeName": "period", "AttributeType": "S"},
        ],
        [
            {"AttributeName": "user_id", "KeyType": "HASH"},
            {"AttributeName": "period", "KeyType": "RANGE"},
        ],
    )


def _create_if_missing(
    client: Any,
    name: str,
    attributes: list[dict[str, str]],
    keys: list[dict[str, str]],
) -> None:
    try:
        client.describe_table(TableName=name)
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code")
        if code != "ResourceNotFoundException":
            raise
    else:
        return
    client.create_table(
        TableName=name,
        AttributeDefinitions=attributes,
        KeySchema=keys,
        BillingMode="PAY_PER_REQUEST",
    )
    client.get_waiter("table_exists").wait(TableName=name)
