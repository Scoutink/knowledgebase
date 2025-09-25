# Proposed Improvements

- Added source indices in `knowledgebase/`:
  - `NIS2_REFERENCE_INDEX.md` — occurrences of articles/annexes with context.
  - `NIS2_KB_OVERVIEW.md` — categorized overview and topic→documents mapping.
- Authored optimized prompt at `prompt.v2.md` enforcing citations, source priority, and a retrieval algorithm.
- Added guidance aids in `knowledgebase/`:
  - `NIS2_ROUTING_GUIDE.md` — how to route questions to the right KB files.
  - `NIS2_EVIDENCE_CHECKLIST.md` — checklist to strengthen “Evidence Required”.
- Produced analytics in `workspace/` to support maintenance: `KB_SUMMARY.json`, `EXCEL_REPORT.json`, and human‑readable `KB_MAPPING.md`, `EXCEL_ANALYSIS.md`.

Adoption
- Use `prompt.v2.md` as the system prompt.
- Keep `knowledgebase/` indices updated when KB changes; re‑run extraction scripts.
- Expect improved “1” scores by ensuring answers include exact citations when present in KB; otherwise explicitly state none found.
