"""Thin CLI: resolve study name / protocol id via CT.gov + PubMed."""

from __future__ import annotations

import typer

from cli.http.dump_json import dump_json
from tools.ctg.resolve_trial_mention import resolve_trial_mention


def resolve_trial(
    query: str = typer.Argument(..., help="Study name, acronym, or protocol id"),
    page_size: int = typer.Option(10, "--page-size", help="Max hits per source"),
) -> None:
    """Resolve a non-NCT study mention to NCT (or unresolved)."""
    try:
        result = resolve_trial_mention(query, page_size=page_size)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(dump_json(result))
