from typing import ClassVar

from models.basic.div import Div


class FormGroup(Div):
    """
    A ``<div class="form-group">`` — a single question block.

    Same as :class:`~models.basic.div.Div` but with the class name fixed, so the
    caller only supplies ``elements`` (and optionally ``depends_on``).
    """

    base_css_classes: ClassVar[str] = "form-group"
