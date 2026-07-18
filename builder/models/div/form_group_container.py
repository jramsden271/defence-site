from models.basic.div import Div


class FormGroupContainer(Div):
    """
    A ``<div class="form-group-container">`` — the outermost wrapper grouping a
    question with its dependent follow-ups.

    Same as :class:`~models.basic.div.Div` but with the class name fixed, so the
    caller only supplies ``elements`` (and optionally ``depends_on``).
    """

    class_: str = "form-group-container"
