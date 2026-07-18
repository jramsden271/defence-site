from models.questions.base_question import BaseQuestion


class TextQuestion(BaseQuestion):
    """
    A question answered with a single free-form value (text, date, integer, ...).

    Pure data — the label and optional help text. Which HTML input type gets
    rendered (text/date/number) is decided entirely by the control it's
    passed to, e.g. :class:`~models.forms.date_input.DateInput`.
    """
