"""Thin CLI wrapper for FDA label search by therapeutic area."""

from __future__ import annotations

import typer

from cli.http.dump_json import dump_json
from hc_http.fda.search_by_therapeutic_area import DEFAULT_SORT_BY
from model.fda_scrape_versions import DEFAULT_SCRAPE_VERSION, FdaScrapeVersions
from tools.fda.search_fdalabel_by_therapeutic_area import (
    search_fdalabel_by_therapeutic_area,
)


def search_by_therapeutic_area(
    ta_description: str = typer.Argument(..., help="Therapeutic area text"),
    version: str = typer.Option(
        DEFAULT_SCRAPE_VERSION,
        "--version",
        "-v",
        help="Scrape version applied to every cache/version field",
    ),
    maxn: int = typer.Option(30, "--maxn", help="Max candidates"),
    offset: int = typer.Option(0, "--offset", help="Result offset"),
    limit: int = typer.Option(10, "--limit", help="Result limit"),
    sort_by: str = typer.Option(
        DEFAULT_SORT_BY, "--sort-by", help="Sort order (e.g. relevance)"
    ),
) -> None:
    """Search FDA labels by therapeutic area (HC API)."""
    try:
        results = search_fdalabel_by_therapeutic_area(
            ta_description,
            versions=FdaScrapeVersions.all(version),
            maxn=maxn,
            offset=offset,
            limit=limit,
            sort_by=sort_by,
        )
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(dump_json(results))
