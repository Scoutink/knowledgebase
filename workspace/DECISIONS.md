# Decisions (ADR)

- Language: Python for portability and rich PDF tooling.
- Extraction: pdfminer.six for per-page text; no transformations.
- Site: Static HTML with client-side search to keep hosting simple.
- Structure: Per-document page + original PDF copy + global index.json.
- Viewer: Inline iframe for quick preview; link to full PDF.