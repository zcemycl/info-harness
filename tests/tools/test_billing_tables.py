"""Billing env parsing and local table bootstrap."""

from __future__ import annotations

from typing import Any

import pytest
from botocore.exceptions import ClientError

from model.billing.billing_config import BillingConfig
from tools.billing.billing_client import billing_client
from tools.billing.ensure_billing_tables import ensure_billing_tables
from tools.billing.table_names import billing_table_names


def test_open_mode_ignores_the_cap(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BILLING_MODE", "open")
    monkeypatch.delenv("FREE_RESEARCH_RUNS", raising=False)
    config = BillingConfig.from_env()
    assert config.mode == "open"
    assert config.free_research_runs is None


def test_stripe_mode_requires_both_caps(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BILLING_MODE", "stripe")
    monkeypatch.setenv("FREE_RESEARCH_RUNS", "2")
    monkeypatch.setenv("PRO_RESEARCH_RUNS", "100")
    config = BillingConfig.from_env()
    assert config.mode == "stripe"
    assert config.free_research_runs == 2
    assert config.pro_research_runs == 100

    monkeypatch.setenv("PRO_RESEARCH_RUNS", "")
    with pytest.raises(ValueError, match="PRO_RESEARCH_RUNS"):
        BillingConfig.from_env()


def test_table_mode_requires_a_positive_cap(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BILLING_MODE", "table")
    monkeypatch.setenv("FREE_RESEARCH_RUNS", "5")
    config = BillingConfig.from_env()
    assert config.mode == "table"
    assert config.free_research_runs == 5

    monkeypatch.setenv("FREE_RESEARCH_RUNS", "")
    with pytest.raises(ValueError, match="FREE_RESEARCH_RUNS"):
        BillingConfig.from_env()


def test_client_uses_aws_when_the_local_endpoint_is_unset(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("DYNAMODB_ENDPOINT_URL", raising=False)
    monkeypatch.setenv("DYNAMODB_REGION", "eu-west-2")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "real")
    captured: dict[str, Any] = {}

    def fake_client(name: str, **kwargs: str) -> object:
        captured["name"] = name
        captured["kwargs"] = kwargs
        return object()

    monkeypatch.setattr("tools.billing.billing_client.boto3.client", fake_client)
    billing_client()
    assert captured["name"] == "dynamodb"
    assert captured["kwargs"]["region_name"] == "eu-west-2"
    assert "endpoint_url" not in captured["kwargs"]
    assert "aws_access_key_id" not in captured["kwargs"]


def test_client_uses_the_local_endpoint(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DYNAMODB_ENDPOINT_URL", "http://localhost:8000")
    monkeypatch.setenv("DYNAMODB_REGION", "eu-west-2")
    monkeypatch.delenv("AWS_ACCESS_KEY_ID", raising=False)
    captured: dict[str, Any] = {}

    def fake_client(name: str, **kwargs: str) -> object:
        del name
        captured["kwargs"] = kwargs
        return object()

    monkeypatch.setattr("tools.billing.billing_client.boto3.client", fake_client)
    billing_client()
    assert captured["kwargs"]["endpoint_url"] == "http://localhost:8000"
    assert captured["kwargs"]["aws_access_key_id"] == "local"


def test_ensure_skips_without_an_endpoint(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DYNAMODB_ENDPOINT_URL", raising=False)
    ensure_billing_tables(client=_boom())


def test_default_names_match_the_aws_tables(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("BILLING_ENTITLEMENTS_TABLE", raising=False)
    monkeypatch.delenv("BILLING_USAGE_TABLE", raising=False)
    assert billing_table_names() == (
        "hc-platform-main-billing-entitlements",
        "hc-platform-main-billing-usage",
    )


def test_ensure_creates_both_tables(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DYNAMODB_ENDPOINT_URL", "http://localhost:8000")
    monkeypatch.delenv("BILLING_ENTITLEMENTS_TABLE", raising=False)
    monkeypatch.delenv("BILLING_USAGE_TABLE", raising=False)
    client = _MemoryDynamo()
    ensure_billing_tables(client=client)
    ensure_billing_tables(client=client)
    entitlements, usage_name = billing_table_names()
    assert client.names == {entitlements, usage_name}
    usage = client.created[usage_name]
    assert [key["AttributeName"] for key in usage["KeySchema"]] == [
        "user_id",
        "period",
    ]


class _MemoryDynamo:
    def __init__(self) -> None:
        self.names: set[str] = set()
        self.created: dict[str, dict[str, Any]] = {}

    def describe_table(self, TableName: str) -> dict[str, str]:
        if TableName not in self.names:
            raise ClientError(
                {"Error": {"Code": "ResourceNotFoundException", "Message": "missing"}},
                "DescribeTable",
            )
        return {"TableName": TableName}

    def create_table(self, **kwargs: Any) -> dict[str, str]:
        name = str(kwargs["TableName"])
        self.names.add(name)
        self.created[name] = kwargs
        return {"TableName": name}

    def get_waiter(self, _name: str) -> Any:
        return _Ready()


class _Ready:
    def wait(self, TableName: str) -> None:
        assert TableName


def _boom() -> Any:
    class _Refuse:
        def describe_table(self, TableName: str) -> None:
            raise AssertionError(TableName)

    return _Refuse()
