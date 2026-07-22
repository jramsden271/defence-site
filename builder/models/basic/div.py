from typing import ClassVar

from builder.models.basic.html_tag import Conditional


class Div(Conditional):
    """
    A generic container element.

    Set ``depends_on`` (via a trigger's ``.when(value)``) to make the whole
    container conditionally visible.

    Renders via the base :class:`~builder.models.basic.html_tag.HtmlTag`
    render (``tag``/``base_attributes``/``children``) — nothing to override
    here. A plain ``str`` in ``children`` is emitted verbatim, not
    auto-wrapped in a paragraph; wrap it in a
    :class:`~models.basic.p.P` yourself if you want one.

    Has no ``class`` of its own — for a single question block, use
    :class:`~builder.models.div.form_group.FormGroup` instead.
    """

    tag: ClassVar[str] = "div"
