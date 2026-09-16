"""Thin CLI wrapper for conditions-by-TA listing."""

from __future__ import annotations

import typer

from cli.http.dump_json import dump_json
from hc_http.therapeutic_area.get_condition_by_ta import DEFAULT_TA
from tools.therapeutic_area.get_condition_by_ta import get_condition_by_ta as run


def get_condition_by_ta(
    ta: str = typer.Argument(DEFAULT_TA, help="Therapeutic area name"),
) -> None:
    """List Level-1 conditions for a therapeutic area (HC API)."""
    try:
        results = run(ta)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(dump_json(results))
