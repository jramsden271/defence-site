from pydantic import Field, field_validator

from builder.models.basic.base_element import BaseElement, normalise_children


class Form(BaseElement):
    """
    A ``<form>`` container holding the questions and controls.

    Note: the front-end visibility script (footer.html) attaches to the form by
    id, so this must match — currently ``profileForm``.
    """

    id: str = Field(default="profileForm", description="The form's id.")
    elements: list[str | BaseElement] = Field(
        default_factory=list, description="Top-level form children."
    )

    _wrap_strings = field_validator("elements", mode="before")(normalise_children)

    def to_html(self) -> str:
        inner = "\n\n".join(child.to_html() for child in self.elements)
        return f'<form id="{self.id}">\n\n{inner}\n\n</form>'
