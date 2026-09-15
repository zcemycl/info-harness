"""Thin CLI wrapper for CTG condition autocomplete."""

from __future__ import annotations

import json

import typer

from tools.ctg.search_ctg_condition import search_ctg_condition


def search_condition(
    q: str = typer.Argument(..., help="Condition query"),
    both_sides: bool = typer.Option(
        False, "--both-sides", help="Match substring on both sides"
    ),
) -> None:
    """Autocomplete CTG condition names (HC API)."""
    try:
        results = search_ctg_condition(q, both_sides=both_sides)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(json.dumps(results, indent=2))
