from typing import ClassVar

from pydantic import Field

from builder.models.basic.html_tag import HtmlTag


class Button(HtmlTag):
    """A ``<button type="button">`` with a click handler."""

    tag: ClassVar[str] = "button"
    base_attributes: ClassVar[dict[str, str]] = {"class": "btn btn-primary", "type": "button"}

    text: str = Field(..., description="The button label.")
    onclick: str = Field(..., description="The JS expression run on click.")
    id: str | None = Field(default=None, description="Optional element id.")

    def _attrs_html(self) -> str:
        """As :meth:`HtmlTag._attrs_html`, plus ``onclick`` and (if set)
        ``id``."""
        id_attr = f' id="{self.id}"' if self.id else ""
        return f'{super()._attrs_html()}{id_attr} onclick="{self.onclick}"'

    def _inner_html(self) -> str:
        """A button's inner HTML is just its label text."""
        return self.text
