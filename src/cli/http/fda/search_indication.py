"""Thin CLI wrapper for FDA label indication search."""

from __future__ import annotations

import json

import typer

from hc_http.fda._cache_key import DEFAULT_CACHE_KEY
from hc_http.fda.search_by_indication import DEFAULT_SORT_BY
from model.fda_scrape_versions import DEFAULT_SCRAPE_VERSION, FdaScrapeVersions
from tools.fda.search_fdalabel_indication import search_fdalabel_indication


def search_indication(
    indication: str = typer.Argument(..., help="Indication text to search"),
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
    cache_key: str = typer.Option(
        DEFAULT_CACHE_KEY, "--cache-key", help="Server-side cache key"
    ),
) -> None:
    """Search FDA labels by indication (HC API)."""
    try:
        results = search_fdalabel_indication(
            indication,
            versions=FdaScrapeVersions.all(version),
            maxn=maxn,
            offset=offset,
            limit=limit,
            sort_by=sort_by,
            cache_key=cache_key,
        )
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(json.dumps(results, indent=2))
