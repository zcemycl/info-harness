"""CLI subgroup for therapeutic-area HC endpoints."""

import typer

from cli.http.therapeutic_area.get_condition_by_ta import get_condition_by_ta
from cli.http.therapeutic_area.get_subindication import get_subindication
from cli.http.therapeutic_area.search import search

app = typer.Typer(
    name="ta",
    help="Therapeutic area / ICD HC endpoints.",
    add_completion=False,
    no_args_is_help=True,
)

app.command("search")(search)
app.command("conditions")(get_condition_by_ta)
app.command("subindications")(get_subindication)
