"""Thin CLI: run the PubMed PMID id-sections worker."""

from __future__ import annotations

import typer

from agents.pubmed_id_sections.run import run_pubmed_id_sections
from cli.agent.echo_agent_answer import echo_agent_answer


def pubmed_id_sections(
    brief: str = typer.Argument(..., help="User brief for the PMID sections worker"),
    max_turns: int = typer.Option(8, "--max-turns"),
    run_id: str | None = typer.Option(None, "--run-id"),
) -> None:
    """Run PubMed PMID id-sections worker (per-section MEDLINE tools)."""
    try:
        result = run_pubmed_id_sections(brief, max_turns=max_turns, run_id=run_id)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    echo_agent_answer(result)
