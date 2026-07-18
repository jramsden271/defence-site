from pydantic import Field

from models.basic.base_element import BaseElement


class IntegerInput(BaseElement):
    """
    A labelled ``<input type="number" step="1">``, restricted to whole numbers.

    The label and input are emitted together so the field reads as one unit.
    """

    id: str = Field(..., description="The input element id (and label target).")
    label: str = Field(..., description="The label text shown above the input.")

    def to_html(self) -> str:
        return (
            f'<label for="{self.id}">{self.label}</label>\n'
            f'<input type="number" step="1" id="{self.id}">'
        )
