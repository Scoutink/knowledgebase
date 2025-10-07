# AI Knowledge Base Site

Static site containing all repository PDFs with per-document pages, full original files, and an AI-friendly `index.json` for ingestion.

## Build

```bash
python3 -m pip install -r requirements.txt --no-input --disable-pip-version-check
python3 scripts/sitegen.py
```

Artifacts are in `site/`:
- `index.html`: landing page with client-side search
- `docs/*.html`: per-document pages with embedded PDF viewer and text
- `files/*`: original PDFs (unaltered)
- `index.json`: metadata and per-page text chunks
- `sitemap.xml`, `robots.txt`, `static/*`

## Deploy

Upload the `site/` directory to your static hosting (S3/CloudFront, Azure Static Web Apps, Netlify, etc.).

## Provide to AI Bot

Include the public URL of `index.json` and the site root in your system prompt so the bot can retrieve context and link back to sources.

## Git Branch

See `workspace/GIT.md` for branch and push instructions.