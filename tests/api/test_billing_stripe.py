"""Stripe Checkout, portal, webhook, and the Pro cap."""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from api.app import app
from api.require_access_token import ChatCaller, require_access_token
from model.billing.entitlement import Entitlement


def test_checkout_is_missing_outside_stripe(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BILLING_MODE", "table")
    monkeypatch.setenv("FREE_RESEARCH_RUNS", "2")
    app.dependency_overrides[require_access_token] = lambda: ChatCaller("token", "user")
    response = TestClient(app).post("/billing/checkout")
    app.dependency_overrides.clear()
    assert response.status_code == 404


def test_webhook_is_missing_outside_stripe(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BILLING_MODE", "open")
    response = TestClient(app).post("/billing/webhook", content=b"{}")
    assert response.status_code == 404


def test_checkout_returns_the_session_url(monkeypatch: pytest.MonkeyPatch) -> None:
    _stripe_env(monkeypatch)
    captured: dict[str, Any] = {}

    class _Sessions:
        def create(self, params: dict[str, Any]) -> Any:
            captured["params"] = params
            return type("Session", (), {"url": "https://checkout.test/pay"})()

    class _Customers:
        def create(self, params: dict[str, Any]) -> Any:
            captured["customer"] = params
            return type("Customer", (), {"id": "cus_1"})()

    class _Client:
        v1 = type(
            "V1",
            (),
            {
                "checkout": type("Checkout", (), {"sessions": _Sessions()})(),
                "customers": _Customers(),
            },
        )()

    monkeypatch.setattr(
        "tools.billing.start_checkout.read_entitlement",
        lambda _user_id, client=None: Entitlement(),
    )
    monkeypatch.setattr(
        "tools.billing.start_checkout.save_entitlement",
        lambda *_args, **_kwargs: None,
    )
    monkeypatch.setattr("tools.billing.start_checkout.stripe_client", lambda: _Client())
    app.dependency_overrides[require_access_token] = lambda: ChatCaller(
        "token", "user-1"
    )
    response = TestClient(app).post("/billing/checkout")
    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json()["url"] == "https://checkout.test/pay"
    params = captured["params"]
    assert params["mode"] == "subscription"
    assert "payment_method_types" not in params
    assert params["line_items"] == [{"price": "price_pro", "quantity": 1}]
    assert params["client_reference_id"] == "user-1"
    assert params["success_url"].endswith(
        "/billing/success?session_id={CHECKOUT_SESSION_ID}"
    )
    suffix = params["integration_identifier"][-8:]
    assert suffix.isalpha() and suffix.islower()


def test_free_user_keeps_the_free_cap(monkeypatch: pytest.MonkeyPatch) -> None:
    _stripe_env(monkeypatch)
    monkeypatch.setattr(
        "tools.billing.load_stripe_billing.read_entitlement",
        lambda _user_id, client=None: Entitlement(),
    )
    monkeypatch.setattr(
        "tools.billing.load_stripe_billing.read_usage",
        lambda _user_id: (1, "2026-09-29", "2026-10-29"),
    )
    app.dependency_overrides[require_access_token] = lambda: ChatCaller("token", "user")
    body = TestClient(app).get("/billing/me").json()
    app.dependency_overrides.clear()
    assert body["mode"] == "stripe"
    assert body["plan"] == "free"
    assert body["runs_limit"] == 2
    assert body["runs_used"] == 1


def test_active_subscription_uses_the_pro_cap(monkeypatch: pytest.MonkeyPatch) -> None:
    _stripe_env(monkeypatch)
    monkeypatch.setattr(
        "tools.billing.load_stripe_billing.read_entitlement",
        lambda _user_id, client=None: Entitlement(
            status="active",
            current_period_start=1,
            current_period_end=4_000_000_000,
        ),
    )
    monkeypatch.setattr(
        "tools.billing.load_stripe_billing.read_usage",
        lambda _user_id: (3, "2026-09-29", "2026-10-29"),
    )
    app.dependency_overrides[require_access_token] = lambda: ChatCaller("token", "user")
    body = TestClient(app).get("/billing/me").json()
    app.dependency_overrides.clear()
    assert body["plan"] == "pro"
    assert body["status"] == "active"
    assert body["runs_limit"] == 100


def _stripe_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BILLING_MODE", "stripe")
    monkeypatch.setenv("FREE_RESEARCH_RUNS", "2")
    monkeypatch.setenv("PRO_RESEARCH_RUNS", "100")
    monkeypatch.setenv("STRIPE_SECRET_KEY", "rk_test_local")
    monkeypatch.setenv("STRIPE_PRICE_ID", "price_pro")
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", "whsec_local")
    monkeypatch.setenv("APP_PUBLIC_URL", "http://localhost:3000")
