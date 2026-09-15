"""Thin CLI wrapper for PubMed esummary fetch."""

from __future__ import annotations

import json

import typer

from tools.pubmed.fetch_pubmed_summaries import fetch_pubmed_summaries


def fetch_summaries(
    pmid: list[str] = typer.Argument(..., help="One or more PubMed IDs"),
) -> None:
    """Fetch PubMed article summaries by PMID."""
    try:
        results = fetch_pubmed_summaries(pmid)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(json.dumps(results, indent=2))
