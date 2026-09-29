"""StripeClient for Checkout, the Customer Portal, and webhooks."""

from __future__ import annotations

from typing import Any

from model.billing.billing_config import BillingConfig


def stripe_client() -> Any:
    """Return a ``StripeClient`` using ``STRIPE_SECRET_KEY``.

    The key is not assigned on the stripe module. Checkout stays off until
    the secret, Price, webhook secret, and public app URL are set.
    """
    config = BillingConfig.from_env()
    config.require_stripe()
    from stripe import StripeClient

    return StripeClient(config.stripe_secret_key)
