from pathlib import Path

from builder.models.basic.raw import Raw
from builder.models.component import Component

HEADER_DIR = Path(__file__).parent


class Header(Component):
    """The shared site ``<header>``, for a :class:`~builder.models.page.Page`
    to compose into its own output."""

    def to_html(self) -> str:
        return Raw(html=(HEADER_DIR / "layout" / "header.html").read_text(encoding="utf-8")).to_html()
