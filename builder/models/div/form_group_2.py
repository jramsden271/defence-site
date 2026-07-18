from models.basic.div import Div


class FormGroup2(Div):
    """
    A ``<div class="form-group-2">`` — a dependent follow-up block (e.g. the
    date input revealed after a question is answered).

    Same as :class:`~models.basic.div.Div` but with the class name fixed, so the
    caller only supplies ``elements`` (and optionally ``depends_on``).
    """

    class_: str = "form-group-2"
