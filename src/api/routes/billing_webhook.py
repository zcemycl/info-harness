"""Stripe webhook. Signature is the auth; no Cognito token."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from model.billing.billing_config import BillingConfig
from tools.billing.apply_webhook import WebhookSignatureError, apply_webhook

router = APIRouter()


@router.post("/billing/webhook")
async def billing_webhook(request: Request) -> dict[str, bool]:
    """Verify ``Stripe-Signature`` and store the subscription."""
    if BillingConfig.from_env().mode != "stripe":
        raise HTTPException(
            status_code=404, detail="webhook is available in stripe mode"
        )
    try:
        apply_webhook(await request.body(), request.headers.get("stripe-signature", ""))
    except WebhookSignatureError as exc:
        raise HTTPException(status_code=400, detail="invalid signature") from exc
    except ValueError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {"received": True}
