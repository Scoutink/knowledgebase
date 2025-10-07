# Branching and Push Instructions

We avoid performing git operations in this automated environment. To publish:

```bash
# from repo root
git checkout -b feature/ai-knowledge-base-site
git add .
git commit -m "feat(site): generate static knowledge base with PDF index"
git push -u origin feature/ai-knowledge-base-site
```

After review, merge via PR into your integration branch.