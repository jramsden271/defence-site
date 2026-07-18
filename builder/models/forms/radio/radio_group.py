from typing import ClassVar

from pydantic import Field

from models.basic.base_element import Triggerable, render_help
from models.forms.radio.radio_item import RadioItem
from models.questions.multiple_choice_question import MultipleChoiceQuestion


class RadioGroup(Triggerable):
    """
    Renders a :class:`~models.questions.multiple_choice_question.MultipleChoiceQuestion`
    as a labelled group of radio buttons, plus its collapsible help block.

    It renders only the control itself (no surrounding wrapper) so it composes
    like any other element — wrap it in a :class:`~models.basic.div.Div` for
    layout, and put ``depends_on`` on that wrapping div to make it conditional.

    Because it is :class:`Triggerable`, other elements can depend on the
    selected answer via ``some_group.when("value")``.
    """

    base_css_classes: ClassVar[str] = "radio-group govuk-radio-group"

    # inherited: name + .when() (Triggerable)
    question: MultipleChoiceQuestion = Field(..., description="The question this group renders.")

    def to_html(self) -> str:
        # Build one RadioItem per option, stamping the group name + last-item
        # flag needed for rendering (these are render-time concerns, not part
        # of the question's own data).
        last_index = len(self.question.options) - 1
        rendered_items = []
        for index, option in enumerate(self.question.options):
            item = RadioItem(
                label=option.label,
                value=option.value,
                description=option.description,
                radio_group_name=self.name,
                is_last=index == last_index,
            )
            rendered_items.append(item.to_html())
        items_html = "\n".join(rendered_items)

        return (
            f'<label for="{self.name}">{self.question.display_question}</label>\n'
            f'<div class="{self._css_classes()}" '
            f'data-trigger="{self.trigger_id}">\n'
            f"{items_html}\n"
            f"</div>"
            f"{render_help(self.question.help)}"
        )
