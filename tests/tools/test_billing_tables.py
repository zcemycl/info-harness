"""Billing env parsing and local table bootstrap."""

from __future__ import annotations

from typing import Any

import pytest
from botocore.exceptions import ClientError

from model.billing.billing_config import BillingConfig
from tools.billing.ensure_billing_tables import (
    ENTITLEMENTS_TABLE,
    USAGE_TABLE,
    ensure_billing_tables,
)


def test_open_mode_ignores_the_cap(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BILLING_MODE", "open")
    monkeypatch.delenv("FREE_RESEARCH_RUNS", raising=False)
    config = BillingConfig.from_env()
    assert config.mode == "open"
    assert config.free_research_runs is None


def test_table_mode_requires_a_positive_cap(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BILLING_MODE", "table")
    monkeypatch.setenv("FREE_RESEARCH_RUNS", "5")
    config = BillingConfig.from_env()
    assert config.mode == "table"
    assert config.free_research_runs == 5

    monkeypatch.setenv("FREE_RESEARCH_RUNS", "")
    with pytest.raises(ValueError, match="FREE_RESEARCH_RUNS"):
        BillingConfig.from_env()


def test_ensure_skips_without_an_endpoint(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DYNAMODB_ENDPOINT_URL", raising=False)
    ensure_billing_tables(client=_boom())


def test_ensure_creates_both_tables(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DYNAMODB_ENDPOINT_URL", "http://localhost:8000")
    client = _MemoryDynamo()
    ensure_billing_tables(client=client)
    ensure_billing_tables(client=client)
    assert client.names == {ENTITLEMENTS_TABLE, USAGE_TABLE}
    usage = client.created[USAGE_TABLE]
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
