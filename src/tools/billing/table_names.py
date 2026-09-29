"""DynamoDB table names for free-plan billing."""

from __future__ import annotations

import os

_ENTITLEMENTS = "hc-platform-main-billing-entitlements"
_USAGE = "hc-platform-main-billing-usage"


def billing_table_names() -> tuple[str, str]:
    """Return ``(entitlements, usage)``.

    Defaults are the existing AWS tables. Override either with
    ``BILLING_ENTITLEMENTS_TABLE`` or ``BILLING_USAGE_TABLE``.
    """
    entitlements = os.getenv("BILLING_ENTITLEMENTS_TABLE", "").strip() or _ENTITLEMENTS
    usage = os.getenv("BILLING_USAGE_TABLE", "").strip() or _USAGE
    return entitlements, usage
