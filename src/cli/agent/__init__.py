"""Typer sub-app for agent runners."""

import typer

from cli.agent.fda_label_specialist import fda_label_specialist
from cli.agent.fda_search_id import fda_search_id
from cli.agent.fda_search_indication import fda_search_indication
from cli.agent.fda_search_therapeutic_area import fda_search_therapeutic_area
from cli.agent.fda_search_tradename import fda_search_tradename
from cli.agent.icd_ta_specialist import icd_ta_specialist
from cli.agent.icd_ta_worker import icd_ta_worker

app = typer.Typer(
    name="agent",
    help="Run FDA/ICD search workers and specialist loops.",
    add_completion=False,
    no_args_is_help=True,
)

app.command("fda-search-tradename")(fda_search_tradename)
app.command("fda-search-indication")(fda_search_indication)
app.command("fda-search-id")(fda_search_id)
app.command("fda-search-therapeutic-area")(fda_search_therapeutic_area)
app.command("fda-label-specialist")(fda_label_specialist)
app.command("icd-ta-worker")(icd_ta_worker)
app.command("icd-ta-specialist")(icd_ta_specialist)
