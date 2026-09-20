"""Final answer synthesis for the FDA label specialist."""

from __future__ import annotations

import json

from agents.chat_model import chat_model
from model.research.evidence_note import EvidenceNote


def synthesize_fda_answer(brief: str, evidence: list[EvidenceNote]) -> str:
    """Write a short answer from the brief and collected evidence notes."""
    llm = chat_model(model_env="OPENROUTER_FDA_SPECIALIST_MODEL")
    payload = {
        "brief": brief,
        "evidence": [n.model_dump(mode="json") for n in evidence],
    }
    response = llm.invoke(
        [
            {
                "role": "system",
                "content": (
                    "Answer the brief using only the evidence notes. "
                    "Cite tradename and setid. Be concise."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(payload, indent=2, default=str),
            },
        ]
    )
    content = response.content
    return content if isinstance(content, str) else str(content)
