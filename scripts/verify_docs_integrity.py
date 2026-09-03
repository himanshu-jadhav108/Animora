"""Verify mkdocs navigation, links, and media asset resolution."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

docs_dir = Path("docs")
mkdocs_file = Path("mkdocs.yml")


class IgnoreUnknownLoader(yaml.SafeLoader):
    pass


IgnoreUnknownLoader.add_constructor(None, lambda loader, node: None)

with open(mkdocs_file, encoding="utf-8") as f:
    config = yaml.load(f, Loader=IgnoreUnknownLoader)


def extract_nav_files(nav: list) -> list[str]:
    files = []
    for item in nav:
        if isinstance(item, str):
            files.append(item)
        elif isinstance(item, dict):
            for _k, v in item.items():
                if isinstance(v, str):
                    files.append(v)
                elif isinstance(v, list):
                    files.extend(extract_nav_files(v))
    return files


nav_files = extract_nav_files(config.get("nav", []))
print(f"Checking {len(nav_files)} navigation targets from mkdocs.yml...")

missing_nav = []
for rel in nav_files:
    p = docs_dir / rel
    if not p.exists():
        missing_nav.append(str(p))

if missing_nav:
    print(f"ERROR: Missing nav files: {missing_nav}")
    sys.exit(1)

print("SUCCESS: All mkdocs.yml navigation targets exist.")

broken_links = []
img_pattern = re.compile(r'<img\s+[^>]*src=["\']([^"\']+)["\']|!\[[^\]]*\]\(([^)]+)\)')

for md_file in docs_dir.rglob("*.md"):
    with open(md_file, encoding="utf-8") as f:
        content = f.read()

    for match in img_pattern.finditer(content):
        src = match.group(1) or match.group(2)
        if src.startswith(("http://", "https://", "data:")):
            continue
        target = (md_file.parent / src).resolve()
        if not target.exists():
            broken_links.append((str(md_file), src))

if broken_links:
    print(f"ERROR: Broken media links found: {broken_links}")
    sys.exit(1)

print("SUCCESS: All document media and image references resolved cleanly.")
