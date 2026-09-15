"""CLI subgroup for CTG HC endpoints."""

import typer

from cli.http.ctg.count_by_compare_filters import count_by_compare_filters
from cli.http.ctg.get_by_nctids import get_by_nctids
from cli.http.ctg.search_by_compare_filters import search_by_compare_filters
from cli.http.ctg.search_condition import search_condition

app = typer.Typer(
    name="ctg",
    help="ClinicalTrials.gov (CTG) HC endpoints.",
    add_completion=False,
    no_args_is_help=True,
)

app.command("get-by-nctids")(get_by_nctids)
app.command("search-condition")(search_condition)
app.command("search-by-compare-filters")(search_by_compare_filters)
app.command("count-by-compare-filters")(count_by_compare_filters)
