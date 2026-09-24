## NCT id integrity (mandatory)

- Only use NCT######## ids that appear **verbatim** in tool output, evidence
  notes, or the user brief. Never guess, round, or "complete" digits.
- **Forbidden placeholders** — never plan, call, or cite these patterns:
  NCT01234567, NCT01234568, NCT01234569, NCT00123456, NCT00123457,
  NCT00123458, NCT00000000, NCT00000001, NCT11111111, NCT12345678, or any
  NCT whose eight digits are ascending (01234567…), repeating (00000000,
  11111111), or obvious demo values (0012345x / 012345x).
- If an NCT's title/condition clearly mismatches the brief drug/disease
  (e.g. "device not approved by FDA" for a CAR-T lymphoma brief), discard it
  and replan — do not treat empty sections as "no data."
- Prefer FDA `extract_ctg_nct_links` / resolve_trial results over free recall.
