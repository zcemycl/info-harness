"""Final answer synthesis for the CTG specialist."""

from __future__ import annotations

import json

from agents.chat_model import chat_model
from model.ctg.ctg_evidence_note import CtgEvidenceNote


def synthesize_ctg_answer(brief: str, evidence: list[CtgEvidenceNote]) -> str:
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
                    "Cite nctid (and setid when present), resolve_trial "
                    "outcomes (resolved NCT or unresolved), or concrete "
                    "condition names from evidence. Do not invent. Be concise."
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
