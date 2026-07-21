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
from builder.models.page import Page

page_dir = Path(__file__).parent
repo_root = page_dir.parent.parent.parent
dist_dir = repo_root / "dist"

page = Page(
    title="Defence generators",
    page_name="index",
    body=[
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
    ],
)

page.write(dist_dir)
