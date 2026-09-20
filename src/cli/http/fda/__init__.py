"""CLI subgroup for FDA label HC endpoints."""

import typer

from cli.http.fda.autocomplete_manufacturer import autocomplete_manufacturer
from cli.http.fda.autocomplete_setid import autocomplete_setid
from cli.http.fda.autocomplete_tradename import autocomplete_tradename
from cli.http.fda.compare_adverse_effects import compare_adverse_effects
from cli.http.fda.count_by_compare_filters import count_by_compare_filters
from cli.http.fda.history import history
from cli.http.fda.search_by_compare_filters import search_by_compare_filters
from cli.http.fda.search_by_id import search_by_id
from cli.http.fda.search_by_manufacturer import search_by_manufacturer
from cli.http.fda.search_by_therapeutic_area import search_by_therapeutic_area
from cli.http.fda.search_indication import app as search_indication_app
from cli.http.fda.search_tradename import app as search_tradename_app

app = typer.Typer(
    name="fda",
    help="FDA label HC endpoints.",
    add_completion=False,
    no_args_is_help=True,
)

app.add_typer(search_tradename_app, name="search-tradename")
app.add_typer(search_indication_app, name="search-indication")
app.command("search-by-id")(search_by_id)
app.command("search-by-ta")(search_by_therapeutic_area)
app.command("search-by-manufacturer")(search_by_manufacturer)
app.command("search-by-compare-filters")(search_by_compare_filters)
app.command("count-by-compare-filters")(count_by_compare_filters)
app.command("autocomplete-tradename")(autocomplete_tradename)
app.command("autocomplete-manufacturer")(autocomplete_manufacturer)
app.command("autocomplete-setid")(autocomplete_setid)
app.command("history")(history)
app.command("compare-adverse-effects")(compare_adverse_effects)
