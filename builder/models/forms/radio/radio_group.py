from pydantic import Field

from models.basic.base_element import HasHelp, Triggerable
from models.forms.radio.radio_item import RadioItem


class RadioGroup(Triggerable, HasHelp):
    """
    A labelled group of radio buttons: the ``label``, the radio options and an
    optional collapsible help block.

    It renders only the control itself (no surrounding wrapper) so it composes
    like any other element — wrap it in a :class:`~models.basic.div.Div` for
    layout, and put ``depends_on`` on that wrapping div to make it conditional.

    Because it is :class:`Triggerable`, other elements can depend on the
    selected answer via ``some_group.when("value")``. Its ``help`` (from
    :class:`HasHelp`) may be a ``Details`` or a string/list-of-strings shortcut.
    """

    # inherited: name + .when() (Triggerable); help + help_html() (HasHelp)
    label: str = Field(..., description="The question/label for the radio group.")
    items: list[RadioItem] = Field(default = [], description="The radio options.")

    def to_html(self) -> str:
        # Stamp group name + last-item flag onto each option.
        last_index = len(self.items) - 1
        rendered_items = []
        for index, item in enumerate(self.items):
            item.radio_group_name = self.name
            item.is_last = index == last_index
            rendered_items.append(item.to_html())
        items_html = "\n".join(rendered_items)

        return (
            f'<label for="{self.name}">{self.label}</label>\n'
            f'<div class="radio-group govuk-radio-group" '
            f'data-trigger="{self.trigger_id}">\n'
            f"{items_html}\n"
            f"</div>"
            f"{self.help_html()}"
        )
    
    def add_option(self, label: str, value: str|None = None, description: str = "") -> None:
        """
        Add a new radio item to the group.
        """
        value = value if value else label.lower().replace(" ", "_")
        self.items.append(RadioItem(label=label, value=value, description=description))

    def add_yes_no_options(self, yes_label: str = "Yes", no_label: str = "No") -> None:
        """
        Add a standard Yes/No option set to the group.
        """
        self.add_option(label=yes_label, value="yes")
        self.add_option(label=no_label, value="no")
