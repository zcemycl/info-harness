"""Typer sub-app for eval benchmarking."""

import typer

from cli.eval.run import run

app = typer.Typer(
    name="eval",
    help="Benchmark FDA workers and the inner specialist loop.",
    add_completion=False,
    no_args_is_help=True,
)

app.command("run")(run)
