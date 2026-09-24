"""Detect FDA evidence gaps for subindication trials and AE table kinds."""

from __future__ import annotations

from typing import Any

from model.fda.ae_table_kind import AeTableKind
from model.fda.fda_attr_name import FdaAttrName
from tools.fda.classify_ae_table_kind import classify_ae_table_kind
from tools.research.collect_nct_ids import collect_nct_ids


def fda_completeness_gaps(notes: list[Any]) -> list[str]:
    """Return gap strings from compact/full evidence notes."""
    gaps: list[str] = []
    attrs: set[str] = set()
    summaries: list[str] = []
    ae_kinds: set[AeTableKind] = set()
    has_placeholders = False
    has_trial_ids = False

    for note in notes:
        raw = note.model_dump(mode="json") if hasattr(note, "model_dump") else note
        if not isinstance(raw, dict):
            continue
        attr = raw.get("attr")
        if attr:
            attrs.add(str(attr))
        summary = str(raw.get("summary") or "")
        summaries.append(summary)
        if "Table placeholders:" in summary or "tableplaceholder" in summary.lower():
            has_placeholders = True
        if collect_nct_ids(summary) or "Study mentions:" in summary:
            has_trial_ids = True
        if attr == FdaAttrName.ADVERSE_EFFECT_TABLES.value:
            kind = _kind_from_summary(summary)
            if kind is not None:
                ae_kinds.add(kind)

    text_blob = "\n".join(summaries)
    subinds = _subindication_titles(text_blob)
    if subinds and not has_trial_ids:
        gaps.append(
            "Subindications/sections found but no NCT or study mention yet: "
            + "; ".join(subinds[:6])
        )
    if (
        FdaAttrName.ADVERSE_EFFECTS.value in attrs
        or has_placeholders
        or FdaAttrName.ADVERSE_EFFECT_TABLES.value in attrs
    ):
        if AeTableKind.AE_REACTION not in ae_kinds:
            gaps.append("Missing adverse_reaction (ae_reaction) table coverage")
        if AeTableKind.LABORATORY not in ae_kinds:
            gaps.append("Missing laboratory abnormality table coverage")
    if (
        FdaAttrName.ADVERSE_EFFECTS.value in attrs
        and FdaAttrName.ADVERSE_EFFECT_TABLES.value not in attrs
        and has_placeholders
    ):
        gaps.append("adverse_effects has placeholders but no adverse_effect_tables")
    if (
        FdaAttrName.CLINICAL_TRIALS.value in attrs
        and FdaAttrName.CLINICAL_TRIAL_TABLES.value not in attrs
        and has_placeholders
    ):
        gaps.append("clinical_trials has placeholders but no clinical_trial_tables")
    return gaps


def _kind_from_summary(summary: str) -> AeTableKind | None:
    if "kind=ae_reaction" in summary or "kind=ae_reaction" in summary.lower():
        return AeTableKind.AE_REACTION
    if "kind=laboratory" in summary:
        return AeTableKind.LABORATORY
    # Fall back to caption heuristics embedded in summary head
    kind = classify_ae_table_kind(summary[:200])
    return kind if kind is not AeTableKind.OTHER else None


def _subindication_titles(text: str) -> list[str]:
    import re

    titles = re.findall(r"<title>([^<]{3,120})</title>", text, flags=re.IGNORECASE)
    return list(dict.fromkeys(t.strip() for t in titles if t.strip()))
