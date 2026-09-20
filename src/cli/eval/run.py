"""Thin CLI: run worker / inner eval suites."""

from __future__ import annotations

from enum import StrEnum

import typer

from model.eval.eval_layer import EvalLayer
from pipeline.eval.run_suite import run_eval_suite


class LayerChoice(StrEnum):
    """CLI layer selector."""

    WORKER = "worker"
    INNER = "inner"
    ALL = "all"


def run(
    layer: LayerChoice = typer.Option(
        LayerChoice.ALL, "--layer", help="worker | inner | all"
    ),
    case: str | None = typer.Option(None, "--case", help="Single case id"),
    no_judge: bool = typer.Option(
        False, "--no-judge", help="Fixture checks only (skip LLM judge)"
    ),
    suite_id: str | None = typer.Option(None, "--suite-id", help="Output folder id"),
) -> None:
    """Run eval cases from examples/eval and write data/eval/{suite_id}/."""
    layers = (
        [EvalLayer.WORKER, EvalLayer.INNER]
        if layer is LayerChoice.ALL
        else [EvalLayer(layer.value)]
    )
    try:
        reports = run_eval_suite(
            layers,
            case_id=case,
            use_judge=not no_judge,
            suite_id=suite_id,
        )
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc

    if not reports:
        typer.secho("No cases matched.", fg=typer.colors.YELLOW, err=True)
        raise typer.Exit(code=1)

    passed = sum(1 for r in reports if r.passed)
    for r in reports:
        color = typer.colors.GREEN if r.passed else typer.colors.RED
        judge_bit = ""
        if r.judge is not None:
            judge_bit = f" judge={r.judge.score:.1f}"
        typer.secho(
            f"[{r.layer.value}] {r.case_id}: "
            f"{'PASS' if r.passed else 'FAIL'} "
            f"fixtures={r.fixtures.passed}{judge_bit}",
            fg=color,
        )
    typer.echo(f"{passed}/{len(reports)} passed")
    if passed < len(reports):
        raise typer.Exit(code=1)
