"""Stripe Customer Portal for an existing subscriber."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from api.require_access_token import ChatCaller, require_access_token
from model.billing.billing_config import BillingConfig
from tools.billing.start_portal import start_portal

router = APIRouter()


@router.post("/billing/portal")
def billing_portal(
    caller: ChatCaller = Depends(require_access_token),
) -> dict[str, str]:
    """Return a portal URL. Other billing modes have no subscription."""
    if BillingConfig.from_env().mode != "stripe":
        raise HTTPException(
            status_code=404, detail="portal is available in stripe mode"
        )
    try:
        url = start_portal(caller.sub)
    except ValueError as exc:
        message = str(exc)
        status = 404 if message == "no stripe customer" else 503
        raise HTTPException(status_code=status, detail=message) from exc
    return {"url": url}
