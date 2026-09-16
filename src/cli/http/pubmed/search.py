"""Thin CLI wrapper for PubMed search."""

from __future__ import annotations

import typer

from cli.http.dump_json import dump_json
from tools.pubmed.search_pubmed import search_pubmed


def search(
    query: str = typer.Argument(..., help="PubMed search query"),
    retmax: int = typer.Option(20, "--retmax", help="Max IDs to return"),
    retstart: int = typer.Option(0, "--retstart", help="Result offset"),
    sort: str = typer.Option("relevance", "--sort", help="Sort order"),
) -> None:
    """Search PubMed via NCBI E-utilities."""
    try:
        results = search_pubmed(query, retmax=retmax, retstart=retstart, sort=sort)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(dump_json(results))
