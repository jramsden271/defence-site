from typing import ClassVar

from pydantic import Field

from builder.models.basic.html_tag import HtmlTag


class Form(HtmlTag):
    """
    A ``<form>`` container holding the questions and controls.

    Note: the front-end visibility script (footer.html) attaches to the form by
    id, so this must match — currently ``profileForm``.
    """

    tag: ClassVar[str] = "form"

    id: str = Field(default="profileForm", description="The form's id.")

    def _attrs_html(self) -> str:
        """As :meth:`HtmlTag._attrs_html`, plus this form's ``id``."""
        return f'{super()._attrs_html()} id="{self.id}"'
