# CLI

Typer commands registered from `src/main.py`. Run from the repository root (Python 3.12+, [`uv`](https://docs.astral.sh/uv/)).

## How to run

```bash
uv run python src/main.py --help
uv run python src/main.py cognito-login -u USERNAME -p PASSWORD
uv run python src/main.py http --help
uv run python src/main.py http search-tradename Keytruda
uv run python src/main.py http search-indication melanoma
```

## Notes

- All user-facing workflows go through `src/main.py`.
- One Typer command per file under `src/cli/`.
- HTTP request CLIs live under `src/cli/http/` and are mounted as `main.py http <command>`.
- Command bodies stay thin — call into `hc_http/`, `pipeline/`, `agents/`, or `tools/`.
