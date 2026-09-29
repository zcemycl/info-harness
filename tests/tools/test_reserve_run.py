"""Stripe mode picks the free or Pro cap before a run is consumed."""

from __future__ import annotations

import pytest

from model.billing.entitlement import Entitlement
from tools.billing.reserve_run import reserve_run


def test_unsubscribed_user_uses_the_free_cap(monkeypatch: pytest.MonkeyPatch) -> None:
    _env(monkeypatch)
    seen: dict[str, int] = {}
    monkeypatch.setattr(
        "tools.billing.reserve_run.read_entitlement",
        lambda _user_id, client=None: Entitlement(),
    )
    monkeypatch.setattr(
        "tools.billing.reserve_run.consume_run",
        lambda _user_id, limit, client=None: seen.setdefault("limit", limit),
    )
    assert reserve_run("user") is True
    assert seen["limit"] == 2


def test_active_subscriber_uses_the_pro_cap(monkeypatch: pytest.MonkeyPatch) -> None:
    _env(monkeypatch)
    seen: dict[str, int] = {}
    monkeypatch.setattr(
        "tools.billing.reserve_run.read_entitlement",
        lambda _user_id, client=None: Entitlement(
            status="active",
            current_period_end=4_000_000_000,
        ),
    )
    monkeypatch.setattr(
        "tools.billing.reserve_run.consume_run",
        lambda _user_id, limit, client=None: seen.setdefault("limit", limit),
    )
    reserve_run("user")
    assert seen["limit"] == 100


def test_past_due_subscriber_returns_to_the_free_cap(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _env(monkeypatch)
    seen: dict[str, int] = {}
    monkeypatch.setattr(
        "tools.billing.reserve_run.read_entitlement",
        lambda _user_id, client=None: Entitlement(
            status="past_due",
            current_period_end=4_000_000_000,
        ),
    )
    monkeypatch.setattr(
        "tools.billing.reserve_run.consume_run",
        lambda _user_id, limit, client=None: seen.setdefault("limit", limit),
    )
    reserve_run("user")
    assert seen["limit"] == 2


def _env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BILLING_MODE", "stripe")
    monkeypatch.setenv("FREE_RESEARCH_RUNS", "2")
    monkeypatch.setenv("PRO_RESEARCH_RUNS", "100")
