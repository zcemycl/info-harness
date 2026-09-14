# CLI

Typer commands registered from `src/main.py`. Run from the repository root (Python 3.12+, [`uv`](https://docs.astral.sh/uv/)).

## How to run

```bash
uv run python src/main.py --help
uv run python src/main.py hello
uv run python src/main.py tools --help
uv run python src/main.py tools echo "hello"
```

## Notes

- All user-facing workflows go through `src/main.py`.
- One Typer command per file under `src/cli/`.
- Tool CLIs live under `src/cli/tools/` and are mounted as `main.py tools <tool-name>`.
- Command bodies stay thin — call into `pipeline/`, `agents/`, or `tools/`.
