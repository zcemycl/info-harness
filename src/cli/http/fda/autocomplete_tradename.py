"""Thin CLI wrapper for FDA tradename autocomplete."""

from __future__ import annotations

import json

import typer

from hc_http.fda._cache_key import DEFAULT_CACHE_KEY
from model.fda_scrape_versions import DEFAULT_SCRAPE_VERSION, FdaScrapeVersions
from tools.fda.autocomplete_fdalabel_tradename import autocomplete_fdalabel_tradename


def autocomplete_tradename(
    tradename: str = typer.Argument(..., help="Tradename prefix/query"),
    version: str = typer.Option(
        DEFAULT_SCRAPE_VERSION,
        "--version",
        "-v",
        help="Scrape version applied to every cache/version field",
    ),
    cache_key: str = typer.Option(
        DEFAULT_CACHE_KEY, "--cache-key", help="Server-side cache key"
    ),
) -> None:
    """Autocomplete FDA tradenames (HC API)."""
    try:
        results = autocomplete_fdalabel_tradename(
            tradename,
            versions=FdaScrapeVersions.all(version),
            cache_key=cache_key,
        )
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(json.dumps(results, indent=2))
