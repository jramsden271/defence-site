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
from builder.models.basic.raw import Raw
from builder.models.div.button_column import ButtonColumn
from project.page_components.content.content_page import ContentPage

page_dir = Path(__file__).parent

page = ContentPage(
    title="Defence generators",
    page_name="index",
    body=[
        H2(children=[Raw.from_text("Defence generators")]),
        P.from_text(
            "This is a placeholder homepage — a proper landing page is "
            "coming later. For now, pick a tool below."
        ),
        ButtonColumn(
            children=[
                A.from_text(
                    "No stopping defence generator",
                    href="no-stopping-defence.html",
                    custom_attributes={"class": "btn btn-primary"},
                ),
                A.from_text(
                    "Is your NtK valid?",
                    href="ntk-compliance-check.html",
                    custom_attributes={"class": "btn btn-primary"},
                ),
            ],
        ),
    ],
)


def get_page() -> ContentPage:
    return page
