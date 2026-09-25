"""Liveness route."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    """Return a liveness payload."""
    return {"status": "ok"}
