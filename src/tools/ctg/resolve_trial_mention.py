"""Resolve a study name / protocol id to an NCT via CT.gov + PubMed."""

from __future__ import annotations

from model.ctg.ctgov_study_hit import CtgovStudyHit
from model.ctg.resolved_trial import ResolvedTrial, ResolvedTrialStatus
from tools.ctg.expand_trial_aliases import expand_trial_aliases
from tools.ctg.get_ctgov_study import get_ctgov_study
from tools.ctg.search_ctgov_by_id import search_ctgov_by_id
from tools.ctg.search_ctgov_by_titles import search_ctgov_by_titles
from tools.pubmed.extract_nct_from_medline import extract_nct_from_medline
from tools.pubmed.fetch_medline import fetch_medline
from tools.pubmed.search_pubmed import search_pubmed


def resolve_trial_mention(
    query: str,
    *,
    page_size: int = 10,
) -> ResolvedTrial:
    """Alias → CT.gov id → titles → PubMed→NCT→hydrate; never invent NCTs."""
    q = query.strip()
    if not q:
        raise ValueError("query must be non-empty")
    variants = expand_trial_aliases(q)
    sources: list[str] = []
    pmids: list[str] = []
    aliases_tried = variants[1:]

    for variant in variants:
        hits = _exact_id_hits(search_ctgov_by_id(variant, page_size=page_size), variant)
        if hits:
            sources.append("ctgov_id")
            return _from_hits(q, hits, sources, pmids, aliases_tried)

    for variant in variants:
        hits = search_ctgov_by_titles(variant, page_size=page_size)
        if hits:
            sources.append("ctgov_titles")
            return _from_hits(q, hits, sources, pmids, aliases_tried)

    nctids, pmids = _nctids_via_pubmed(variants, retmax=page_size)
    if nctids:
        sources.append("pubmed")
        hydrated: list[CtgovStudyHit] = []
        for nctid in nctids:
            try:
                hydrated.append(get_ctgov_study(nctid))
            except (RuntimeError, ValueError):
                continue
        if hydrated:
            return _from_hits(q, hydrated, sources, pmids, aliases_tried)
        primary = nctids[0]
        return ResolvedTrial(
            query=q,
            status=ResolvedTrialStatus.RESOLVED,
            nctid=primary,
            ctg_url=f"https://clinicaltrials.gov/study/{primary}",
            sources=sources,
            pmids=pmids,
            aliases_tried=aliases_tried,
            candidate_nctids=nctids,
        )

    return ResolvedTrial(
        query=q,
        status=ResolvedTrialStatus.UNRESOLVED,
        sources=sources or ["ctgov_id", "ctgov_titles", "pubmed"],
        pmids=pmids,
        aliases_tried=aliases_tried,
    )


def _exact_id_hits(hits: list[CtgovStudyHit], query: str) -> list[CtgovStudyHit]:
    """Keep only hits whose nctid / acronym / orgStudyId equals the query."""
    needle = _norm(query)
    if not needle:
        return []
    matched: list[CtgovStudyHit] = []
    for hit in hits:
        candidates = [hit.nctid, hit.acronym, hit.org_study_id]
        if any(_norm(c) == needle for c in candidates if c):
            matched.append(hit)
    return matched


def _norm(text: str) -> str:
    return "".join(ch for ch in text.casefold() if ch.isalnum())


def _from_hits(
    query: str,
    hits: list[CtgovStudyHit],
    sources: list[str],
    pmids: list[str],
    aliases_tried: list[str],
) -> ResolvedTrial:
    primary = hits[0]
    return ResolvedTrial(
        query=query,
        status=ResolvedTrialStatus.RESOLVED,
        nctid=primary.nctid,
        ctg_url=primary.ctg_url,
        brief_title=primary.brief_title,
        official_title=primary.official_title,
        acronym=primary.acronym,
        overall_status=primary.overall_status,
        sources=sources,
        pmids=pmids,
        aliases_tried=aliases_tried,
        candidate_nctids=[h.nctid for h in hits],
    )


def _nctids_via_pubmed(
    variants: list[str],
    *,
    retmax: int,
) -> tuple[list[str], list[str]]:
    seen_pmid: set[str] = set()
    all_pmids: list[str] = []
    for variant in variants:
        for term in (f"{variant}[Title]", variant):
            result = search_pubmed(term, retmax=retmax)
            for pmid in result.esearchresult.idlist or []:
                if pmid in seen_pmid:
                    continue
                seen_pmid.add(pmid)
                all_pmids.append(pmid)
            if all_pmids:
                break
        if all_pmids:
            break
    if not all_pmids:
        return [], []
    medline = fetch_medline(all_pmids[:retmax])
    links = extract_nct_from_medline(medline)
    return [link.nctid for link in links], all_pmids[:retmax]
