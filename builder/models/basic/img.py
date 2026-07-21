from typing import ClassVar

from pydantic import Field

from builder.models.basic.html_tag import Conditional


class Img(Conditional):
    """
    Represents an image element in the model.
    """

    tag: ClassVar[str] = "img"
    is_self_closing: ClassVar[bool] = True

    src: str = Field(..., description="The image's source URL.")
    alt: str = Field(..., description="Alt text describing the image, for accessibility.")

    def _attrs_html(self) -> str:
        """As :meth:`HtmlTag._attrs_html`, plus ``src``/``alt``."""
        return f'{super()._attrs_html()} src="{self.src}" alt="{self.alt}"'
