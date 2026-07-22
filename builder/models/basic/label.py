from typing import ClassVar

from pydantic import Field

from builder.models.basic.html_tag import HtmlTag
from builder.models.basic.raw import Raw


class Label(HtmlTag):
    """
    Represents a label element in the model.
    """

    tag: ClassVar[str] = "label"

    for_: str | None = Field(
        default=None, description="The ID of the element this label is associated with."
    )

    @classmethod
    def from_text(cls, text: str, for_: str | None = None):
        """``text`` may contain inline HTML (e.g. ``<em>``), which is emitted as-is."""
        return cls(children=[Raw.from_text(text)], for_=for_)

    def _attrs_html(self) -> str:
        """As :meth:`HtmlTag._attrs_html`, plus ``for`` (if set)."""
        for_attr = f' for="{self.for_}"' if self.for_ else ""
        return f"{super()._attrs_html()}{for_attr}"
