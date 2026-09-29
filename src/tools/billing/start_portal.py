"""Open the Stripe Customer Portal for the signed-in user."""

from __future__ import annotations

from model.billing.billing_config import BillingConfig
from tools.billing.read_entitlement import read_entitlement
from tools.billing.stripe_client import stripe_client


def start_portal(user_id: str) -> str:
    """Return a portal URL for cancel, card, and invoice management."""
    config = BillingConfig.from_env()
    config.require_stripe()
    customer_id = read_entitlement(user_id).customer_id
    if not customer_id:
        raise ValueError("no stripe customer")
    session = stripe_client().v1.billing_portal.sessions.create(
        {
            "customer": customer_id,
            "return_url": f"{config.app_public_url}/app",
        }
    )
    return str(session.url)
