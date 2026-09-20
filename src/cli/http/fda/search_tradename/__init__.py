"""CLI subgroup: FDA label search by tradename (attr tools)."""

import typer

from cli.http.fda.search_tradename.adverse_effects import adverse_effects
from cli.http.fda.search_tradename.indication import indication

app = typer.Typer(
    name="search-tradename",
    help="Search FDA labels by tradename (slim attr pages).",
    add_completion=False,
    no_args_is_help=True,
)

app.command("indication")(indication)
app.command("adverse-effects")(adverse_effects)
