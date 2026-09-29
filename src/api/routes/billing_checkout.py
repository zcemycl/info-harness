"""Hosted Stripe Checkout for the Pro subscription."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from api.require_access_token import ChatCaller, require_access_token
from model.billing.billing_config import BillingConfig
from tools.billing.start_checkout import start_checkout

router = APIRouter()


@router.post("/billing/checkout")
def billing_checkout(
    caller: ChatCaller = Depends(require_access_token),
) -> dict[str, str]:
    """Return a Checkout URL. Other billing modes have nothing to buy."""
    if BillingConfig.from_env().mode != "stripe":
        raise HTTPException(
            status_code=404, detail="checkout is available in stripe mode"
        )
    try:
        url = start_checkout(caller.sub)
    except ValueError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {"url": url}
