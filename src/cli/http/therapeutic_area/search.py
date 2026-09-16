"""Thin CLI wrapper for therapeutic area autocomplete."""

from __future__ import annotations

import typer

from cli.http.dump_json import dump_json
from tools.therapeutic_area.search_therapeutic_area import search_therapeutic_area


def search(
    q: str = typer.Argument(..., help="Therapeutic area query"),
    both_sides: bool = typer.Option(
        False, "--both-sides", help="Match substring on both sides"
    ),
) -> None:
    """Autocomplete therapeutic area names (HC API)."""
    try:
        results = search_therapeutic_area(q, both_sides=both_sides)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(dump_json(results))
