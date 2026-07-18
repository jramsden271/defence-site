from pydantic import Field

from models.basic.base_element import Conditional


class Heading(Conditional):
    """A heading element (``<h1>``..``<h6>``)."""

    text: str = Field(..., description="The heading text.")
    level: int = Field(default=2, ge=1, le=6, description="Heading level 1-6.")

    def to_html(self) -> str:
        return f"<h{self.level}{self._visibility_attrs()}>{self.text}</h{self.level}>"
