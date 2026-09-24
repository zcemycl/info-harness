"""After section hits with placeholders, fetch paired *_tables by setid."""

from __future__ import annotations

from typing import Any

from agents.fda_label_specialist.execute_tasks import execute_fda_tasks
from model.fda.fda_label_attr_hit import FdaLabelAttrHit
from model.fda.fda_label_attr_page import FdaLabelAttrPage
from model.fda.fda_label_section import FdaLabelSection
from model.research.worker_plan import FdaAttrName, FdaWorkerName, WorkerPlan
from tools.fda.extract_table_placeholders import extract_table_placeholders
from tools.fda.section_table_pairs import is_tables_attr, section_table_pair
from tools.trace_call import trace_info

PageTriple = tuple[WorkerPlan, FdaAttrName, FdaLabelAttrPage[Any]]


def expand_fda_section_table_triples(
    triples: list[PageTriple],
) -> tuple[list[PageTriple], list[str]]:
    """Append paired tables pages for setids whose section prose has placeholders."""
    extra: list[PageTriple] = []
    failures: list[str] = []
    have_tables = _existing_table_setids(triples)

    for plan, attr, page in triples:
        tables_attr = section_table_pair(attr)
        if tables_attr is None:
            continue
        for item in page.items:
            if not isinstance(item, FdaLabelAttrHit):
                continue
            if not _section_has_placeholders(item.value):
                continue
            setid = str(item.setid)
            key = (setid, tables_attr)
            if key in have_tables:
                continue
            have_tables.add(key)
            follow = WorkerPlan(
                worker=FdaWorkerName.ID,
                query=setid,
                attrs=[tables_attr],
                offset=0,
                limit=20,
                maxn=30,
            )
            pages, errs = execute_fda_tasks([follow])
            failures.extend(errs)
            for fplan, fattr, fpage in pages:
                extra.append((fplan, fattr, fpage))
                trace_info(
                    "auto tables",
                    setid=setid,
                    attr=fattr.value,
                    items=len(fpage.items),
                )
    return [*triples, *extra], failures


def _existing_table_setids(
    triples: list[PageTriple],
) -> set[tuple[str, FdaAttrName]]:
    found: set[tuple[str, FdaAttrName]] = set()
    for _plan, attr, page in triples:
        if not is_tables_attr(attr):
            continue
        for item in page.items:
            if isinstance(item, FdaLabelAttrHit):
                found.add((str(item.setid), attr))
    return found


def _section_has_placeholders(value: object) -> bool:
    for text in _section_texts(value):
        if extract_table_placeholders(text):
            return True
    return False


def _section_texts(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, FdaLabelSection):
        return [value.content or ""]
    if isinstance(value, list):
        out: list[str] = []
        for entry in value:
            out.extend(_section_texts(entry))
        return out
    if hasattr(value, "content"):
        return [str(getattr(value, "content") or "")]
    return []
