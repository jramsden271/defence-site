from typing import ClassVar

from pydantic import Field

from builder.models.basic.html_tag import Conditional


class A(Conditional):
    """
    Represents an anchor/link element in the model.
    """

    tag: ClassVar[str] = "a"

    text: str = Field(..., description="The link's visible text.")
    href: str = Field(..., description="The link's destination URL.")

    def _attrs_html(self) -> str:
        """As :meth:`HtmlTag._attrs_html`, plus ``href``."""
        return f'{super()._attrs_html()} href="{self.href}"'

    def _inner_html(self) -> str:
        """A link's inner HTML is just its text."""
        return self.text
