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
uv run python src/main.py http ta search immuno
uv run python src/main.py http pubmed search "pembrolizumab"
```

## Notes

- All user-facing workflows go through `src/main.py`.
- One Typer command per file under `src/cli/`.
- HTTP CLIs live under `src/cli/http/<domain>/` and are mounted as `main.py http <domain> <command>`.
- Attr-scoped FDA searches are grouped as `http fda search-tradename|search-indication <attr>`.
- Command bodies stay thin — call into `tools/` (preferred) or `hc_http/`.
