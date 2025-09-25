# Prompt Analysis Notes

## Strengths
- Enforces exclusive reliance on the provided knowledgebase (meets key requirement).
- Gathers initial user context (role, sector, NIS2 stage) before answering.
- Provides a professional, repeatable answer structure.
- Clear refusal/deflection policy for non‑NIS2/meta questions.

## Gaps Likely Causing 0.5 Scores
- No explicit, mandatory citations of NIS2 articles/annexes in answers when available in the KB.
- No requirement to name the exact KB file(s) and (if possible) page/section where the information comes from.
- No priority rule to resolve source conflicts (e.g., official law vs. templates vs. frameworks).
- No explicit search plan: it does not instruct the assistant to first consult a reference index or map.
- No safeguard to avoid generic guidance when concrete references exist, leading to “correct but missing codes.”
- Limited guidance on tailoring responses using the collected user context (role/sector/stage) beyond gating.

## Opportunities to Improve
- Require a “Citations & KB Sources” section in every answer when information exists in the KB.
- Add a “Source Priority” policy: (1) Belgian law/official docs → (2) CyberFundamentals framework → (3) Policy templates for examples/evidence.
- Add “Use the KB indices first” instruction (`knowledgebase/NIS2_REFERENCE_INDEX.md` and `knowledgebase/NIS2_KB_OVERVIEW.md`) to quickly locate relevant articles/annexes.
- Require explicit article/annex codes (e.g., Article 30(1), Annex I) when present in the KB; otherwise say none found.
- Mandate short quotes for critical numeric thresholds or timers, strictly from the KB.
- Add an “Answering Algorithm” that systematically searches, cites, and tailors.

## Excel Test Observations (AI Phoenix - Standard tests.xlsx)
- Scoring shows 0 / 0.5 / 1 scale; 0.5 implies correct but lacking specific NIS2 code references.
- Sheets “SCRIPT ...” contain structured question prompts across domains (ID, PR, DE, RS, etc.).
- To achieve consistent 1’s, answers must include correct guidance plus explicit references.

## Proposed Fixes (Implemented in optimized prompt)
- Mandatory citations with article/annex codes when present in KB.
- Source priority order and retrieval steps leveraging the newly added KB indices.
- Tailoring: build short, role/sector/stage-specific “Suggested Next Steps.”
- Strict fallback message when references are not found in the KB.
