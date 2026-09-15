"""Thin CLI wrapper for FDA scrape version listing."""

from __future__ import annotations

import json

import typer

from tools.fda.get_fdalabel_scrape_versions import get_fdalabel_scrape_versions


def get_scrape_versions() -> None:
    """List available FDA scrape versions (HC API)."""
    try:
        results = get_fdalabel_scrape_versions()
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(json.dumps(results, indent=2))
