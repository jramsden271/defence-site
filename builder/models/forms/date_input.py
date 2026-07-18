from pydantic import Field

from builder.models.basic.base_element import Triggerable, render_help
from builder.models.questions.single_question import SingleQuestion


class DateInput(Triggerable):
    """
    Renders a :class:`~models.questions.single_question.SingleQuestion` as a
    labelled ``<input type="date">``, plus its collapsible help block.

    The label and input are emitted together so the field reads as one unit.
    """

    # inherited: name + .when() (Triggerable)
    question: SingleQuestion = Field(..., description="The question this input renders.")

    def to_html(self) -> str:
        return (
            f'<label for="{self.name}">{self.question.display_question}</label>\n'
            f'<input type="date" id="{self.name}">'
            f"{render_help(self.question.help)}"
        )
