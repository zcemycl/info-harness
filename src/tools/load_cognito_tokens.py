"""Load Cognito JWT tokens from `.cognito_tokens.json`."""

from __future__ import annotations

import json
from pathlib import Path

from model.cognito_tokens import CognitoTokens
from tools.cognito_tokens_path import COGNITO_TOKENS_PATH


def load_cognito_tokens(path: Path | None = None) -> CognitoTokens:
    """Read tokens from `.cognito_tokens.json` (or `path`) for later API calls."""
    target = path or COGNITO_TOKENS_PATH
    if not target.is_file():
        raise FileNotFoundError(
            f"No Cognito tokens at {target.resolve()}. "
            "Run: uv run python src/main.py cognito-login -u <username>"
        )
    raw = json.loads(target.read_text(encoding="utf-8"))
    return CognitoTokens.model_validate(raw)
