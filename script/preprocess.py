#!/usr/bin/env python3
"""
Converts Obsidian markdown to Hugo-compatible markdown.
Run before pushing: python3 scripts/preprocess.py
"""
import re, shutil, os
from pathlib import Path

VAULT   = Path("../")   # ← change this
CONTENT = Path("content/posts")                   # Hugo content dir

CONTENT.mkdir(parents=True, exist_ok=True)

for md in VAULT.rglob("*.md"):
    # Skip Obsidian system files
    if ".obsidian" in str(md) or md.name.startswith("."):
        continue

    text = md.read_text(encoding="utf-8")

    # Convert [[WikiLinks]] → [WikiLinks](../wikilinks/)
    text = re.sub(
        r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]',
        lambda m: f'[{m.group(2) or m.group(1)}](../{m.group(1).lower().replace(" ", "-")}/)',
        text
    )

    # Convert ![[image.png]] → ![image.png](image.png)
    text = re.sub(r'!\[\[([^\]]+)\]\]', r'![\1](\1)', text)

    # Add Hugo frontmatter if missing
    if not text.startswith("---"):
        slug = md.stem.lower().replace(" ", "-")
        text = f'---\ntitle: "{md.stem}"\ndate: 1970-01-01\ndraft: false\n---\n\n' + text

    dest = CONTENT / (md.stem.lower().replace(" ", "-") + ".md")
    dest.write_text(text, encoding="utf-8")
    print(f"  ✓ {md.name} → {dest.name}")

print("Done. Review content/posts/ then git add & push.")