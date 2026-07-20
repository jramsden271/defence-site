from typing import ClassVar

from pydantic import Field, field_validator

from builder.models.basic.html_tag import HtmlTag, Conditional, normalise_children


class Div(Conditional):
    """
    A generic container element.

    Set ``depends_on`` (via a trigger's ``.when(value)``) to make the whole
    container conditionally visible.

    Children may be given as :class:`HtmlTag` instances or as plain strings;
    strings are wrapped in a :class:`~models.basic.p.P` paragraph, so a simple
    text block reads as ``elements=["some text"]`` instead of
    ``elements=[P(text="some text")]``.
    """

    base_attributes: ClassVar[dict[str, str]] = {"class": "form-group"}
    # Declared as ``str | HtmlTag`` so callers can pass plain strings; the
    # validator below normalises everything to HtmlTag instances.
    elements: list[str | HtmlTag] = Field(
        ..., description="Child elements (strings are treated as paragraphs)."
    )

    _wrap_strings = field_validator("elements", mode="before")(normalise_children)

    def to_html(self) -> str:
        children = []
        for child in self.elements:
            if isinstance(child, str):
                children.append(f'<p>{child}</p>')
            else:
                children.append(child.to_html())
        inner_html = "\n".join(children)
        return (
            f'<div class="{self.get_attribute("class")}"{self._visibility_attrs()}>\n'
            f"{inner_html}\n"
            f"</div>"
        )
