from typing import ClassVar

from pydantic import Field

from builder.models.basic.html_tag import HtmlTag


class Label(HtmlTag):
    """
    Represents a label element in the model.
    """

    tag: ClassVar[str] = "label"

    text: str = Field(..., description="The text content of the label.")
    for_: str | None = Field(
        default=None, description="The ID of the element this label is associated with."
    )

    def _attrs_html(self) -> str:
        """As :meth:`HtmlTag._attrs_html`, plus ``for`` (if set)."""
        for_attr = f' for="{self.for_}"' if self.for_ else ""
        return f"{super()._attrs_html()}{for_attr}"

    def _inner_html(self) -> str:
        """A label's inner HTML is just its text."""
        return self.text
