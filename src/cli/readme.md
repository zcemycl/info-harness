# CLI

Typer commands registered from `src/main.py`. Run from the repository root (Python 3.12+, [`uv`](https://docs.astral.sh/uv/)).

## How to run

```bash
uv run python src/main.py --help
uv run python src/main.py cognito-login -u USERNAME -p PASSWORD
uv run python src/main.py http --help
uv run python src/main.py http fda --help
uv run python src/main.py http fda search-tradename indication Keytruda
uv run python src/main.py http fda search-tradename adverse-effects Keytruda
uv run python src/main.py http ctg search-condition melanoma
uv run python src/main.py http ctg search-nctid basic-info NCT01234567
uv run python src/main.py http ctg search-nctid outcomes NCT01234567
uv run python src/main.py http ta search immuno
uv run python src/main.py http pubmed search "pembrolizumab"
uv run python src/main.py agent ctg-search-nctid "outcomes for NCT01234567"
uv run python src/main.py agent ctg-search-condition "melanoma condition names"
uv run python src/main.py agent ctg-specialist "outcomes for NCT01234567"
```

## Notes

- All user-facing workflows go through `src/main.py`.
- One Typer command per file under `src/cli/`.
- HTTP CLIs live under `src/cli/http/<domain>/` and are mounted as `main.py http <domain> <command>`.
- Attr-scoped FDA searches are grouped as `http fda search-tradename|search-indication|search-id <attr>`.
- Attr-scoped CTG searches are grouped as `http ctg search-nctid <attr>` (`basic-info`, `demographics`, `conditions`, `locations`, `adverse-events`, `outcomes`).
- CTG agents: `ctg-search-nctid`, `ctg-search-condition`, `ctg-specialist`.
- Command bodies stay thin — call into `tools/` (preferred) or `hc_http/`.
