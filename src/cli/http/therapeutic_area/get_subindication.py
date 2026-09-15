"""Thin CLI wrapper for subindication listing."""

from __future__ import annotations

import json

import typer

from hc_http.therapeutic_area.get_subindication_by_ta_condition import (
    DEFAULT_CONDITION,
    DEFAULT_TA,
)
from tools.therapeutic_area.get_subindication_by_ta_condition import (
    get_subindication_by_ta_condition,
)


def get_subindication(
    ta: str = typer.Option(DEFAULT_TA, "--ta", help="Therapeutic area name"),
    condition: str = typer.Option(
        DEFAULT_CONDITION, "--condition", help="Level-1 condition"
    ),
) -> None:
    """List Level-2 subindications for TA + condition (HC API)."""
    try:
        results = get_subindication_by_ta_condition(ta, condition)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(json.dumps(results, indent=2))
