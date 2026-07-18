from pydantic import Field

from models.basic.base_element import Triggerable, render_help
from models.questions.text_question import TextQuestion


class IntegerInput(Triggerable):
    """
    Renders a :class:`~models.questions.text_question.TextQuestion` as a
    labelled ``<input type="number" step="1">``, restricted to whole numbers,
    plus its collapsible help block.

    The label and input are emitted together so the field reads as one unit.
    """

    # inherited: name + .when() (Triggerable)
    question: TextQuestion = Field(..., description="The question this input renders.")

    def to_html(self) -> str:
        return (
            f'<label for="{self.name}">{self.question.display_question}</label>\n'
            f'<input type="number" step="1" id="{self.name}">'
            f"{render_help(self.question.help_title, self.question.help_body)}"
        )
