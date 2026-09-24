"""Final answer synthesis for the PubMed specialist."""

from __future__ import annotations

import json

from agents.chat_model import chat_model
from model.pubmed.pubmed_evidence_note import PubmedEvidenceNote
from tools.evidence.compact_evidence_notes import compact_evidence_notes


def synthesize_pubmed_answer(brief: str, evidence: list[PubmedEvidenceNote]) -> str:
    """Write a short answer from the brief and collected evidence notes."""
    llm = chat_model(model_env="OPENROUTER_FDA_SPECIALIST_MODEL")
    payload = {
        "brief": brief,
        "evidence": compact_evidence_notes(evidence, tail=None),
    }
    response = llm.invoke(
        [
            {
                "role": "system",
                "content": (
                    "Answer the brief using only the evidence notes. "
                    "Cite PMIDs. For literature outcomes, use abstract "
                    "summaries (METHODS/RESULTS narrative). Do not invent "
                    "endpoints or PMIDs. Be concise."
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
