# Build Roadmap

1. Scaffold project structure
   - site/ (output)
   - scripts/sitegen.py (generator)
   - templates/ (jinja templates)
   - static/ (css/js)
   - workspace/ (docs)
2. Implement generator
   - Enumerate PDFs
   - Extract text per page (no edits)
   - Copy original PDFs to site
   - Generate per-file HTML pages
   - Build global index.json (metadata + text)
3. Add navigation & search
   - Landing page listing docs
   - Client-side search over index.json
4. Publish artifacts
   - sitemap.xml, robots.txt
   - README for deployment
5. Git hygiene
   - Work on new branch
   - Commit atomic edits
   - Push branch

Constraints
- Do not modify original content; only copy and render.
- Preserve full text in index to aid LLM context building.