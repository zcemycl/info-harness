"""Thin CLI: run the FDA label specialist PEWE loop."""

from __future__ import annotations

import typer

from cli.agent.echo_agent_answer import echo_agent_answer
from pipeline.run_fda_label_specialist import run_fda_label_specialist_pipeline


def fda_label_specialist(
    brief: str = typer.Argument(..., help="Research brief for the specialist"),
    max_loops: int | None = typer.Option(
        None, "--max-loops", help="Override FDA_SPECIALIST_MAX_LOOPS"
    ),
    run_id: str | None = typer.Option(
        None, "--run-id", help="Diary subfolder id (auto if omitted)"
    ),
    full_json: bool = typer.Option(
        False,
        "--full-json",
        help="Also print full result JSON (answer + evidence + diary)",
    ),
) -> None:
    """Run FDA label specialist planner→executor→writer→evaluator loop."""
    try:
        result = run_fda_label_specialist_pipeline(
            brief, max_loops=max_loops, run_id=run_id
        )
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc

    echo_agent_answer(result.answer)
    typer.secho(
        f"stage_answers={len(result.stage_answers)} loops={result.loops} "
        f"evidence={len(result.evidence)}",
        fg=typer.colors.CYAN,
        err=True,
    )
    if full_json:
        typer.echo(result.model_dump_json(indent=2))
