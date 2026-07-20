from typing import ClassVar

from builder.models.basic.div import Div


class FormGroup(Div):
    """
    A ``<div class="form-group">`` — a single question block.

    Same as :class:`~models.basic.div.Div` but with the class name fixed, so the
    caller only supplies ``children`` (and optionally ``depends_on``).
    """

    base_attributes: ClassVar[dict[str, str]] = {"class": "form-group"}
