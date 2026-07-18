"""
Build dist/index.html — the site's homepage.

Run via the repo-root entry point:

    python builder/build_everything.py

Currently this page has no dynamic content: it's a static file, copied
as-is from ``layout/blocks/index.html`` to ``dist/index.html``. As the
homepage grows (e.g. a generated list of tool links), this can adopt the
same Python-element-tree approach as ``pages/no_stopping_defence``.
"""

from pathlib import Path

page_dir = Path(__file__).parent
repo_root = page_dir.parent.parent
dist_dir = repo_root / "dist"

with open(page_dir / "layout" / "blocks" / "index.html", "r", encoding="utf-8") as f:
    html = f.read()

output_path = dist_dir / "index.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Wrote {output_path}")
