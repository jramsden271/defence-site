from pydantic import Field

from builder.models.basic.base_element import BaseElement


class Label(BaseElement):
    """
    Represents a label element in the model.
    """

    text: str = Field(..., description="The text content of the label.")
    for_: str | None = Field(
        default=None, description="The ID of the element this label is associated with."
    )

    def to_html(self) -> str:
        if self.for_:
            return f'<label for="{self.for_}">{self.text}</label>'
        return f"<label>{self.text}</label>"
