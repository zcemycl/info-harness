"""Signed Stripe webhooks update the stored subscription."""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient
from stripe import SignatureVerificationError

from api.app import app
from model.billing.entitlement import Entitlement
from tools.billing.apply_webhook import WebhookSignatureError, apply_webhook


def test_unsigned_webhook_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    _stripe_env(monkeypatch)

    class _Bad:
        def construct_event(self, payload: bytes, signature: str, secret: str) -> None:
            del payload, secret
            raise SignatureVerificationError("bad", signature)

    monkeypatch.setattr("tools.billing.apply_webhook.stripe_client", lambda: _Bad())
    with pytest.raises(WebhookSignatureError):
        apply_webhook(b"{}", "bad")
    response = TestClient(app).post(
        "/billing/webhook",
        content=b"{}",
        headers={"stripe-signature": "bad"},
    )
    assert response.status_code == 400


def test_subscription_webhook_stores_the_period(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _stripe_env(monkeypatch)
    saved: dict[str, Any] = {}

    class _Client:
        def construct_event(
            self, payload: bytes, signature: str, secret: str
        ) -> dict[str, Any]:
            del payload, signature, secret
            return {
                "type": "customer.subscription.updated",
                "data": {
                    "object": {
                        "id": "sub_1",
                        "customer": "cus_1",
                        "status": "active",
                        "metadata": {"cognito_sub": "user-1"},
                        "items": {
                            "data": [
                                {
                                    "current_period_start": 100,
                                    "current_period_end": 200,
                                    "price": {"id": "price_pro"},
                                }
                            ]
                        },
                    }
                },
            }

    def save(user_id: str, entitlement: Entitlement, client: object = None) -> None:
        del client
        saved["user_id"] = user_id
        saved["entitlement"] = entitlement

    monkeypatch.setattr("tools.billing.apply_webhook.stripe_client", lambda: _Client())
    monkeypatch.setattr("tools.billing.apply_webhook.save_entitlement", save)
    response = TestClient(app).post(
        "/billing/webhook",
        content=b"{}",
        headers={"stripe-signature": "good"},
    )
    assert response.status_code == 200
    assert saved["user_id"] == "user-1"
    stored = saved["entitlement"]
    assert stored.status == "active"
    assert stored.current_period_start == 100
    assert stored.price_id == "price_pro"


def _stripe_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BILLING_MODE", "stripe")
    monkeypatch.setenv("FREE_RESEARCH_RUNS", "2")
    monkeypatch.setenv("PRO_RESEARCH_RUNS", "100")
    monkeypatch.setenv("STRIPE_SECRET_KEY", "rk_test_local")
    monkeypatch.setenv("STRIPE_PRICE_ID", "price_pro")
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", "whsec_local")
    monkeypatch.setenv("APP_PUBLIC_URL", "http://localhost:3000")
