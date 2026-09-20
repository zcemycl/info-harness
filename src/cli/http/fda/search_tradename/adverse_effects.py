"""Thin CLI: tradename search → adverse_effects attr page."""

from __future__ import annotations

import typer

from cli.http.dump_json import dump_json
from model.fda_scrape_versions import DEFAULT_SCRAPE_VERSION, FdaScrapeVersions
from tools.fda.search_fdalabel_tradename.adverse_effects import (
    search_fdalabel_tradename_adverse_effects,
)


def adverse_effects(
    tradename: str = typer.Argument(..., help="Trade name to search"),
    version: str = typer.Option(
        DEFAULT_SCRAPE_VERSION,
        "--version",
        "-v",
        help="Scrape version applied to every cache/version field",
    ),
    maxn: int = typer.Option(30, "--maxn", help="Max candidates"),
    offset: int = typer.Option(0, "--offset", help="Result offset"),
    limit: int = typer.Option(5, "--limit", help="Result limit"),
) -> None:
    """Search by tradename; return adverse_effects page."""
    try:
        results = search_fdalabel_tradename_adverse_effects(
            tradename,
            versions=FdaScrapeVersions.all(version),
            maxn=maxn,
            offset=offset,
            limit=limit,
        )
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(dump_json(results))
