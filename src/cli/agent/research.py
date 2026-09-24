"""Thin CLI: run the research outer PEWE loop."""

from __future__ import annotations

import typer

from cli.agent.echo_agent_answer import echo_agent_answer
from pipeline.run_research import run_research_pipeline


def research(
    brief: str = typer.Argument(..., help="Research brief for the outer loop"),
    max_loops: int | None = typer.Option(
        None, "--max-loops", help="Override RESEARCH_MAX_LOOPS"
    ),
    run_id: str | None = typer.Option(
        None, "--run-id", help="Diary subfolder id (auto if omitted)"
    ),
    concurrency: int | None = typer.Option(
        None,
        "--concurrency",
        help="Override RESEARCH_SPECIALIST_CONCURRENCY",
    ),
    specialist_max_loops: int | None = typer.Option(
        None,
        "--specialist-max-loops",
        help="Inner PEWE loops per spawned specialist",
    ),
    full_json: bool = typer.Option(
        False,
        "--full-json",
        help="Also print full result JSON (answer + pack + diary + memory)",
    ),
) -> None:
    """Run research planner→executor→writer→evaluator outer loop."""
    try:
        result = run_research_pipeline(
            brief,
            max_loops=max_loops,
            run_id=run_id,
            concurrency=concurrency,
            specialist_max_loops=specialist_max_loops,
        )
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc

    echo_agent_answer(result.answer)
    typer.secho(
        f"stage_answers={len(result.stage_answers)} loops={result.loops} "
        f"outcomes={len(result.pack.outcomes)} "
        f"settled={len(result.memory.settled)} "
        f"tried={len(result.memory.tried_ideas)}",
        fg=typer.colors.CYAN,
        err=True,
    )
    if full_json:
        typer.echo(result.model_dump_json(indent=2))
