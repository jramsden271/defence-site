"""
Build dist/index.html — the site's homepage.

Run via the repo-root entry point:

    python builder/build_everything.py

Built from the Python element classes (same approach as
``pages/no_stopping_defence``), rather than a hand-authored HTML
fragment — see ``blocks/`` for the (now unused) legacy file this
replaced.
"""

from pathlib import Path

from builder.models.basic.a import A
from builder.models.basic.heading import H2
from builder.models.basic.p import P
from builder.models.div.button_column import ButtonColumn
from page_templates.content.render_content import render_content

page_dir = Path(__file__).parent
repo_root = page_dir.parent.parent
dist_dir = repo_root / "dist"

intro = [
    H2(children=["Defence generators"]),
    P(text=(
        "This is a placeholder homepage — a proper landing page is "
        "coming later. For now, pick a tool below."
    )),
    ButtonColumn(
        children=[
            A(
                text="No stopping defence generator",
                href="no_stopping_defence.html",
                custom_attributes={"class": "btn btn-primary"},
            ),
            A(
                text="Is your NtK valid?",
                href="ntk_compliance_check.html",
                custom_attributes={"class": "btn btn-primary"},
            ),
        ],
    ),
]

body_html = "\n".join(element.to_html() for element in intro)

html = render_content(title="Defence generators", body_html=body_html)

dist_dir.mkdir(parents=True, exist_ok=True)

output_path = dist_dir / "index.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Wrote {output_path}")
