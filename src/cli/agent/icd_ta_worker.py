"""Thin CLI: run the ICD therapeutic-area worker (search only)."""

from __future__ import annotations

import typer

from agents.icd_ta_worker.run import run_icd_ta_worker
from cli.agent.echo_agent_answer import echo_agent_answer


def icd_ta_worker(
    brief: str = typer.Argument(..., help="User brief for the ICD TA worker"),
    max_turns: int = typer.Option(8, "--max-turns"),
    run_id: str | None = typer.Option(None, "--run-id"),
) -> None:
    """Run ICD TA worker (search_therapeutic_area only; q% vs %q%)."""
    try:
        result = run_icd_ta_worker(brief, max_turns=max_turns, run_id=run_id)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    echo_agent_answer(result)
