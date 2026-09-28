"""DynamoDB client for the local billing tables."""

from __future__ import annotations

import os
from typing import Any

import boto3


def billing_client() -> Any | None:
    """Return a DynamoDB client, or None when no local endpoint is configured."""
    endpoint = os.getenv("DYNAMODB_ENDPOINT_URL", "").strip()
    if not endpoint:
        return None
    region = os.getenv("DYNAMODB_REGION") or os.getenv("COGNITO_REGION") or "eu-west-2"
    kwargs: dict[str, str] = {"region_name": region, "endpoint_url": endpoint}
    if not os.getenv("AWS_ACCESS_KEY_ID"):
        kwargs["aws_access_key_id"] = "local"
        kwargs["aws_secret_access_key"] = "local"
    return boto3.client("dynamodb", **kwargs)
