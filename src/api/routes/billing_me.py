"""Signed-in user's run allowance."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from api.require_access_token import ChatCaller, require_access_token
from model.billing.billing_status import BillingStatus
from tools.billing.load_billing import load_billing

router = APIRouter()


@router.get("/billing/me")
def billing_me(caller: ChatCaller = Depends(require_access_token)) -> BillingStatus:
    """Return the backend billing mode, free-run cap, and runs used."""
    return load_billing(caller.sub)
