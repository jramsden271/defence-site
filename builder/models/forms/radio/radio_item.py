from pydantic import Field

from builder.models.basic.html_tag import HtmlTag


class RadioItem(HtmlTag):
    """
    Represents a single radio button option.

    ``radio_group_name`` and ``is_last`` are normally set by the owning
    :class:`RadioGroup` at render time, so callers only supply ``label`` and
    ``value``.
    """

    label: str = Field(..., description="The label for the radio button.")
    value: str = Field(..., description="The value associated with the radio button.")
    description: str = Field(
        default="", description="Optional description text for the radio button."
    )
    radio_group_name: str = Field(
        default="", description="Name of the group this item belongs to (set by group)."
    )
    is_last: bool = Field(
        default=False, description="Whether this is the last item (drops right margin)."
    )

    def radio_id(self) -> str:
        """A unique, stable id derived from the group name and value."""
        return f"{self.radio_group_name}_{self.value}"

    def to_html(self) -> str:
        margin = "" if self.is_last else " margin-right:15px;"
        description_html = (
            f'<div class="govuk-hint">{self.description}</div>'
            if self.description
            else ""
        )
        return (
            '<div class="govuk-radio-item">\n'
            f'<input class="govuk-radio-input" type="radio" id="{self.radio_id()}" '
            f'name="{self.radio_group_name}" value="{self.value}">\n'
            f'<label class="govuk-radio-label" style="display:inline;{margin}" '
            f'for="{self.radio_id()}">{self.label}</label>\n'
            f'{description_html}'
            "</div>"
        )
