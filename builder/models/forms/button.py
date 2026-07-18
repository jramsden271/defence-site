from typing import ClassVar

from pydantic import Field

from models.basic.base_element import BaseElement


class Button(BaseElement):
    """A ``<button type="button">`` with a click handler."""

    base_css_classes: ClassVar[str] = "btn btn-primary"

    text: str = Field(..., description="The button label.")
    onclick: str = Field(..., description="The JS expression run on click.")
    id: str | None = Field(default=None, description="Optional element id.")

    def to_html(self) -> str:
        id_attr = f' id="{self.id}"' if self.id else ""
        return (
            f'<button type="button"{id_attr} class="{self._css_classes()}" '
            f'onclick="{self.onclick}">{self.text}</button>'
        )
