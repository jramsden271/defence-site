from pydantic import Field

from models.basic.base_element import Conditional


class P(Conditional):
    """
    Represents a paragraph element in the model.

    ``text`` may contain inline HTML (e.g. ``<em>``), which is emitted as-is.
    """

    text: str = Field(..., description="The text content of the paragraph.")

    def to_html(self) -> str:
        return f"<p{self._visibility_attrs()}>{self.text}</p>"
