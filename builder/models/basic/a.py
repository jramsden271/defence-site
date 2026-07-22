from typing import ClassVar

from pydantic import Field

from builder.models.basic.html_tag import Conditional
from builder.models.basic.raw import Raw


class A(Conditional):
    """
    Represents an anchor/link element in the model.
    """

    tag: ClassVar[str] = "a"

    href: str = Field(..., description="The link's destination URL.")

    @classmethod
    def from_text(cls, text: str, href: str, **kwargs):
        """``text`` may contain inline HTML (e.g. ``<em>``), which is emitted as-is."""
        return cls(children=[Raw.from_text(text)], href=href, **kwargs)

    def _attrs_html(self) -> str:
        """As :meth:`HtmlTag._attrs_html`, plus ``href``."""
        return f'{super()._attrs_html()} href="{self.href}"'
