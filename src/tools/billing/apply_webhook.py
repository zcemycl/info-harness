"""Apply a signed Stripe webhook to the billing entitlement."""

from __future__ import annotations

from typing import Any

from model.billing.entitlement import Entitlement
from tools.billing.save_entitlement import save_entitlement
from tools.billing.stripe_client import stripe_client


class WebhookSignatureError(Exception):
    """The ``Stripe-Signature`` header did not match the webhook secret."""


def apply_webhook(payload: bytes, signature: str) -> None:
    """Verify the payload and upsert checkout or subscription events."""
    from stripe import SignatureVerificationError

    from model.billing.billing_config import BillingConfig

    client = stripe_client()
    secret = BillingConfig.from_env().stripe_webhook_secret
    try:
        event = client.construct_event(payload, signature, secret)
    except SignatureVerificationError as exc:
        raise WebhookSignatureError(str(exc)) from exc
    kind = str(_get(event, "type") or "")
    data = _get(event, "data") or {}
    obj = _get(data, "object")
    if kind == "checkout.session.completed":
        _from_session(client, obj)
        return
    if kind in ("customer.subscription.updated", "customer.subscription.deleted"):
        _from_subscription(obj)


def _from_session(client: Any, session: Any) -> None:
    user_id = _user_id(session)
    raw = _get(session, "subscription")
    if not user_id or raw is None:
        return
    subscription = (
        client.v1.subscriptions.retrieve(raw) if isinstance(raw, str) else raw
    )
    _save(user_id, subscription, _get(session, "customer"))


def _from_subscription(subscription: Any) -> None:
    user_id = _user_id(subscription)
    if not user_id:
        return
    _save(user_id, subscription, _get(subscription, "customer"))


def _save(user_id: str, subscription: Any, customer: Any) -> None:
    start, end = _period(subscription)
    status = _get(subscription, "status")
    save_entitlement(
        user_id,
        Entitlement(
            customer_id=_object_id(customer),
            subscription_id=_object_id(subscription),
            status=str(status) if status else None,
            price_id=_price_id(subscription),
            current_period_start=start,
            current_period_end=end,
        ),
    )


def _user_id(obj: Any) -> str:
    meta = _get(obj, "metadata") or {}
    found = _get(meta, "cognito_sub") or _get(obj, "client_reference_id")
    return str(found or "").strip()


def _period(subscription: Any) -> tuple[int | None, int | None]:
    start = _unix(_get(subscription, "current_period_start"))
    end = _unix(_get(subscription, "current_period_end"))
    if start is not None and end is not None:
        return start, end
    items = _get(subscription, "items")
    data = _get(items, "data") if items is not None else None
    if not data:
        return start, end
    item = data[0]
    return (
        _unix(_get(item, "current_period_start")) or start,
        _unix(_get(item, "current_period_end")) or end,
    )


def _price_id(subscription: Any) -> str | None:
    items = _get(subscription, "items")
    data = _get(items, "data") if items is not None else None
    if not data:
        return None
    price = _get(data[0], "price")
    if isinstance(price, str):
        return price
    return _object_id(price)


def _object_id(value: Any) -> str | None:
    if isinstance(value, str):
        return value or None
    found = _get(value, "id") if value is not None else None
    return str(found) if found else None


def _unix(value: Any) -> int | None:
    if value is None:
        return None
    return int(value)


def _get(obj: Any, key: str) -> Any:
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj.get(key)
    getter = getattr(obj, "get", None)
    if callable(getter):
        return getter(key)
    return getattr(obj, key, None)
