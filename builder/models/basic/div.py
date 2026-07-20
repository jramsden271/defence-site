from typing import ClassVar

from builder.models.basic.html_tag import Conditional


class Div(Conditional):
    """
    A generic container element.

    Set ``depends_on`` (via a trigger's ``.when(value)``) to make the whole
    container conditionally visible.

    Renders via the base :class:`~builder.models.basic.html_tag.HtmlTag`
    render (``tag``/``base_attributes``/``elements``) — nothing to override
    here. A plain ``str`` in ``elements`` is emitted verbatim, not
    auto-wrapped in a paragraph; wrap it in a
    :class:`~models.basic.p.P` yourself if you want one.
    """

    tag: ClassVar[str] = "div"
    base_attributes: ClassVar[dict[str, str]] = {"class": "form-group"}
