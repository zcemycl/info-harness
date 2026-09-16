"""Serialize tool/CLI results to indented JSON."""

from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel


def dump_json(value: Any) -> str:
    """Return indented JSON for scalars, lists, dicts, or Pydantic models."""
    if isinstance(value, BaseModel):
        payload: Any = value.model_dump(mode="json")
    elif isinstance(value, list) and value and isinstance(value[0], BaseModel):
        payload = [item.model_dump(mode="json") for item in value]
    else:
        payload = value
    return json.dumps(payload, indent=2)
