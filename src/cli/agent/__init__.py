"""Typer sub-app for agent runners."""

import typer

from cli.agent.fda_label_specialist import fda_label_specialist
from cli.agent.fda_search_id import fda_search_id
from cli.agent.fda_search_indication import fda_search_indication
from cli.agent.fda_search_therapeutic_area import fda_search_therapeutic_area
from cli.agent.fda_search_tradename import fda_search_tradename

app = typer.Typer(
    name="agent",
    help="Run FDA search workers and the FDA label specialist loop.",
    add_completion=False,
    no_args_is_help=True,
)

app.command("fda-search-tradename")(fda_search_tradename)
app.command("fda-search-indication")(fda_search_indication)
app.command("fda-search-id")(fda_search_id)
app.command("fda-search-therapeutic-area")(fda_search_therapeutic_area)
app.command("fda-label-specialist")(fda_label_specialist)
