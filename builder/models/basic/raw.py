from pydantic import Field

from models.basic.base_element import BaseElement


class Raw(BaseElement):
    """
    An escape hatch element that emits its ``html`` verbatim. Useful for small
    inline snippets that don't warrant a dedicated class.
    """

    html: str = Field(..., description="Literal HTML to emit unchanged.")

    def to_html(self) -> str:
        return self.html
