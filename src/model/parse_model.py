"""Validate a JSON object into a Pydantic model."""

from __future__ import annotations

from typing import Any, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def parse_model(model: type[T], data: Any) -> T:
    """Validate a JSON object into a `model` instance."""
    if not isinstance(data, dict):
        raise RuntimeError(f"Unexpected response type: {type(data).__name__}")
    return model.model_validate(data)
