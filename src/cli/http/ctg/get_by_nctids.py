"""Thin CLI wrapper for CTG fetch by NCT IDs."""

from __future__ import annotations

import json

import typer

from hc_http.ctg.get_by_nctids import DEFAULT_CACHE_KEY
from model.fda_scrape_versions import DEFAULT_SCRAPE_VERSION
from tools.ctg.get_ctg_by_nctids import get_ctg_by_nctids


def get_by_nctids(
    nctid: list[str] = typer.Argument(..., help="One or more NCT IDs"),
    version: str = typer.Option(
        DEFAULT_SCRAPE_VERSION, "--version", "-v", help="CTG row version"
    ),
    cache_key: str = typer.Option(
        DEFAULT_CACHE_KEY, "--cache-key", help="Server-side cache key"
    ),
) -> None:
    """Fetch CTG studies by NCT ID (HC API)."""
    try:
        results = get_ctg_by_nctids(nctid, version=version, cache_key=cache_key)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(json.dumps(results, indent=2))
