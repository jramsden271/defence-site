from typing import ClassVar

from pydantic import Field

from builder.models.basic.html_tag import Conditional


class P(Conditional):
    """
    Represents a paragraph element in the model.

    ``text`` may contain inline HTML (e.g. ``<em>``), which is emitted as-is.
    """

    tag: ClassVar[str] = "p"

    text: str = Field(..., description="The text content of the paragraph.")

    def _inner_html(self) -> str:
        """A paragraph's inner HTML is just its text."""
        return self.text
