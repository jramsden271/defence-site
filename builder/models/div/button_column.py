from typing import ClassVar

from builder.models.basic.div import Div


class ButtonColumn(Div):
    """
    A ``<div class="button-column">`` — a centred vertical column of
    buttons/links, each sized to its own content rather than stretched full
    width (unlike :class:`~models.basic.a.A`/:class:`~models.forms.button.Button`
    styled with ``btn-center``, which are block-level and fill their
    container).
    """

    base_attributes: ClassVar[dict[str, str]] = {"class": "button-column"}
