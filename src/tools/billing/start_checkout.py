"""Create a hosted subscription Checkout Session."""

from __future__ import annotations

import secrets
import string
from typing import Any

from model.billing.billing_config import BillingConfig
from model.billing.entitlement import Entitlement
from tools.billing.read_entitlement import read_entitlement
from tools.billing.save_entitlement import save_entitlement
from tools.billing.stripe_client import stripe_client


def start_checkout(user_id: str) -> str:
    """Return the hosted Checkout URL for the monthly Pro Price."""
    config = BillingConfig.from_env()
    config.require_stripe()
    client = stripe_client()
    customer_id = _customer(user_id, client)
    base = config.app_public_url
    suffix = "".join(secrets.choice(string.ascii_lowercase) for _ in range(8))
    session = client.v1.checkout.sessions.create(
        {
            "mode": "subscription",
            "customer": customer_id,
            "client_reference_id": user_id,
            "line_items": [{"price": config.stripe_price_id, "quantity": 1}],
            "success_url": f"{base}/billing/success?session_id={{CHECKOUT_SESSION_ID}}",
            "cancel_url": f"{base}/billing/cancel",
            "metadata": {"cognito_sub": user_id},
            "subscription_data": {"metadata": {"cognito_sub": user_id}},
            "integration_identifier": f"infoharness{suffix}",
        }
    )
    return str(session.url)


def _customer(user_id: str, client: Any) -> str:
    current = read_entitlement(user_id)
    if current.customer_id:
        return current.customer_id
    created = client.v1.customers.create({"metadata": {"cognito_sub": user_id}})
    save_entitlement(user_id, Entitlement(customer_id=str(created.id)))
    return str(created.id)
