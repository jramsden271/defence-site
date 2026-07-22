from pydantic import Field

from builder.models.basic.html_tag import HtmlTag


class Raw(HtmlTag):
    """
    An escape hatch element that emits its ``html`` verbatim. Useful for small
    inline snippets that don't warrant a dedicated class.
    """

    html: str = Field(..., description="Literal HTML to emit unchanged.")

    @classmethod
    def from_text(cls, text: str):
        """``text`` may contain inline HTML (e.g. ``<em>``), which is emitted as-is."""
        return cls(html=text)

    def to_html(self) -> str:
        return self.html
