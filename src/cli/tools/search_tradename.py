"""Thin CLI wrapper for FDA label tradename search."""

from __future__ import annotations

import json

import typer

from model.fda_scrape_versions import DEFAULT_SCRAPE_VERSION, FdaScrapeVersions
from tools.search_fdalabel_tradename import run_search_fdalabel_tradename


def search_tradename(
    tradename: str = typer.Argument(..., help="Trade name to search"),
    version: str = typer.Option(
        DEFAULT_SCRAPE_VERSION,
        "--version",
        "-v",
        help="Scrape version applied to every cache/version field",
    ),
    maxn: int = typer.Option(30, "--maxn", help="Max candidates"),
    offset: int = typer.Option(0, "--offset", help="Result offset"),
    limit: int = typer.Option(10, "--limit", help="Result limit"),
) -> None:
    """Search FDA labels by tradename (HC API)."""
    try:
        results = run_search_fdalabel_tradename(
            tradename,
            versions=FdaScrapeVersions.all(version),
            maxn=maxn,
            offset=offset,
            limit=limit,
        )
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc

    typer.echo(json.dumps(results, indent=2))
