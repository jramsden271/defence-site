"""
Build dist/index.html — the site's homepage.

Run via the repo-root entry point:

    python builder/build_everything.py

Currently this page has no dynamic content: its body is a static fragment,
read as-is from ``layout/blocks/index.html`` and assembled into a full page
via the shared layout renderer. As the homepage grows (e.g. a generated list
of tool links), this can adopt the same Python-element-tree approach as
``pages/no_stopping_defence``.
"""

from pathlib import Path

from pages.shared.layout.render_page import render_page

page_dir = Path(__file__).parent
repo_root = page_dir.parent.parent
dist_dir = repo_root / "dist"

with open(page_dir / "layout" / "blocks" / "index.html", "r", encoding="utf-8") as f:
    body_html = f.read()

html = render_page(title="Defence generators", body_html=body_html)

dist_dir.mkdir(parents=True, exist_ok=True)

output_path = dist_dir / "index.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Wrote {output_path}")
