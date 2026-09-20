"""Build a ChatOpenAI client from OPENROUTER_* / OPENAI_* env vars."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


def chat_model(*, model_env: str | None = None) -> ChatOpenAI:
    """Return a chat model; prefers OpenRouter when OPENROUTER_API_KEY is set."""
    load_dotenv()
    if os.getenv("OPENROUTER_API_KEY"):
        model = (
            (os.getenv(model_env) if model_env else None)
            or os.getenv("OPENROUTER_FDA_SPECIALIST_MODEL")
            or os.getenv("OPENROUTER_MODEL")
            or "openai/gpt-4o-mini"
        )
        return ChatOpenAI(
            model=model,
            api_key=os.environ["OPENROUTER_API_KEY"],
            base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            temperature=0,
        )
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Set OPENROUTER_API_KEY or OPENAI_API_KEY for agent LLM calls"
        )
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        api_key=api_key,
        base_url=os.getenv("OPENAI_BASE_URL") or None,
        temperature=0,
    )
