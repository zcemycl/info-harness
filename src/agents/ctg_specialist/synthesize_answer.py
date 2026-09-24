"""Final answer synthesis for the CTG specialist."""

from __future__ import annotations

import json

from agents.chat_model import chat_model
from model.ctg.ctg_evidence_note import CtgEvidenceNote
from tools.evidence.compact_evidence_notes import compact_evidence_notes


def synthesize_ctg_answer(brief: str, evidence: list[CtgEvidenceNote]) -> str:
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
                    "Cite nctid (and setid when present). When the brief "
                    "lists NCT ids, report study sections for those ids "
                    "from nctid/fetch notes — do not claim 'no NCT found' "
                    "if the brief already named them. For references, use "
                    "evidence.names (PMIDs) and the summary — do not say "
                    "PMIDs are missing if names is non-empty. Cite "
                    "resolve_trial outcomes or condition names only when "
                    "no NCT was available. Do not invent. Be concise."
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
