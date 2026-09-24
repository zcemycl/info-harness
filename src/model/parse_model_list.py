"""Validate a JSON list into Pydantic model instances."""

from __future__ import annotations

from typing import Any, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def parse_model_list(model: type[T], data: Any) -> list[T]:
    """Validate a JSON list into `model` instances."""
    if not isinstance(data, list):
        raise RuntimeError(f"Unexpected response type: {type(data).__name__}")
    return [model.model_validate(item) for item in data]
