"""CLI subgroup: FDA label search by indication (attr tools)."""

import typer

from cli.http.fda.search_indication.adverse_effects import adverse_effects
from cli.http.fda.search_indication.indication import indication

app = typer.Typer(
    name="search-indication",
    help="Search FDA labels by indication (slim attr pages).",
    add_completion=False,
    no_args_is_help=True,
)

app.command("indication")(indication)
app.command("adverse-effects")(adverse_effects)
