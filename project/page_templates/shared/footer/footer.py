from pathlib import Path

from builder.models.basic.raw import Raw
from builder.models.component import Component

FOOTER_DIR = Path(__file__).parent


class Footer(Component):
    """The shared site ``<footer>``, for a :class:`~builder.models.page.Page`
    to compose into its own output."""

    def to_html(self) -> str:
        return Raw(html=(FOOTER_DIR / "layout" / "footer.html").read_text(encoding="utf-8")).to_html()
