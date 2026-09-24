"""Parse a JSON object string for CLI filter options."""

from __future__ import annotations

import json
from typing import Any


def parse_json_object(raw: str, *, label: str) -> dict[str, Any]:
    """Parse `raw` as a JSON object or raise ValueError."""
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON for {label}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{label} must be a JSON object")
    return data
