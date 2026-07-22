from typing import ClassVar

from pydantic import Field

from builder.models.basic.html_tag import HtmlTag


class Button(HtmlTag):
    """A generic ``<button type="button">``. Carries no styling of its
    own — pass whatever ``class`` this button needs via
    ``custom_attributes`` (e.g. ``{"class": "btn btn-primary"}``)."""

    tag: ClassVar[str] = "button"
    base_attributes: ClassVar[dict[str, str]] = {"type": "button"}

    onclick: str | None = Field(default=None, description="The JS expression run on click, if any.")

    def _attrs_html(self) -> str:
        """As :meth:`HtmlTag._attrs_html`, plus ``onclick`` (if set)."""
        onclick_attr = f' onclick="{self.onclick}"' if self.onclick else ""
        return f"{super()._attrs_html()}{onclick_attr}"
