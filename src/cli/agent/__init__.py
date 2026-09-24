"""Typer sub-app for agent runners."""

import typer

from cli.agent.ctg_fetch import ctg_fetch
from cli.agent.ctg_resolve_trial import ctg_resolve_trial
from cli.agent.ctg_search_condition import ctg_search_condition
from cli.agent.ctg_search_nctid import ctg_search_nctid
from cli.agent.ctg_specialist import ctg_specialist
from cli.agent.fda_label_specialist import fda_label_specialist
from cli.agent.fda_search_id import fda_search_id
from cli.agent.fda_search_indication import fda_search_indication
from cli.agent.fda_search_therapeutic_area import fda_search_therapeutic_area
from cli.agent.fda_search_tradename import fda_search_tradename
from cli.agent.icd_ta_specialist import icd_ta_specialist
from cli.agent.icd_ta_worker import icd_ta_worker
from cli.agent.research import research

app = typer.Typer(
    name="agent",
    help="Run FDA/ICD/CTG workers, specialists, and research outer loop.",
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
app.command("ctg-search-nctid")(ctg_search_nctid)
app.command("ctg-fetch")(ctg_fetch)
app.command("ctg-search-condition")(ctg_search_condition)
app.command("ctg-resolve-trial")(ctg_resolve_trial)
app.command("ctg-specialist")(ctg_specialist)
app.command("research")(research)
