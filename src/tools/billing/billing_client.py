"""DynamoDB client for local and production billing tables."""

from __future__ import annotations

import os
from typing import Any

import boto3


def billing_client() -> Any:
    """Return a DynamoDB client.

    ``DYNAMODB_ENDPOINT_URL`` points at DynamoDB Local. When it is unset, use
    the default AWS endpoint and the ambient credentials (the Lambda role).
    """
    region = (
        os.getenv("DYNAMODB_REGION")
        or os.getenv("AWS_REGION")
        or os.getenv("AWS_DEFAULT_REGION")
        or os.getenv("COGNITO_REGION")
        or "eu-west-2"
    )
    kwargs: dict[str, str] = {"region_name": region}
    endpoint = os.getenv("DYNAMODB_ENDPOINT_URL", "").strip()
    if endpoint:
        kwargs["endpoint_url"] = endpoint
        if not os.getenv("AWS_ACCESS_KEY_ID"):
            kwargs["aws_access_key_id"] = "local"
            kwargs["aws_secret_access_key"] = "local"
    return boto3.client("dynamodb", **kwargs)
