"""Persist Cognito JWT tokens to `.cognito_tokens.json`."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from model.cognito_tokens import CognitoTokens
from tools.cognito_tokens_path import COGNITO_TOKENS_PATH


def save_cognito_tokens(
    tokens: CognitoTokens,
    path: Path | None = None,
) -> Path:
    """
    Write tokens as JSON to `.cognito_tokens.json` (or `path`) and return that path.
    """
    target = path or COGNITO_TOKENS_PATH
    payload = tokens.model_dump()
    payload["obtained_at"] = datetime.now(timezone.utc).isoformat()
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return target.resolve()
