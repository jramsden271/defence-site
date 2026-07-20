from typing import ClassVar

from pydantic import Field

from builder.models.basic.html_tag import HtmlTag


class Button(HtmlTag):
    """A ``<button type="button">`` with a click handler."""

    base_attributes: ClassVar[dict[str, str]] = {"class": "btn btn-primary"}

    text: str = Field(..., description="The button label.")
    onclick: str = Field(..., description="The JS expression run on click.")
    id: str | None = Field(default=None, description="Optional element id.")

    def to_html(self) -> str:
        id_attr = f' id="{self.id}"' if self.id else ""
        return (
            f'<button type="button"{id_attr} class="{self.get_attribute("class")}" '
            f'onclick="{self.onclick}">{self.text}</button>'
        )
