from pydantic import Field

from builder.models.questions.base_question import BaseQuestion
from builder.models.questions.question_option import QuestionOption


class MultipleChoiceQuestion(BaseQuestion):
    """
    A question with a fixed set of possible answers.

    Pure data — the label, the options and optional help text. How it's
    rendered (e.g. as a group of radio buttons) is up to the control it's
    passed to, e.g. :class:`~models.forms.radio.radio_group.RadioGroup`.
    """

    options: list[QuestionOption] = Field(
        default_factory=list, description="The possible answers."
    )

    def add_option(self, label: str, value: str | None = None, description: str = "") -> None:
        """
        Add a new option to the question.
        """
        value = value if value else label.lower().replace(" ", "_")
        self.options.append(QuestionOption(label=label, value=value, description=description))

    def add_yes_no_options(self, yes_label: str = "Yes", no_label: str = "No") -> None:
        """
        Add a standard Yes/No option set to the question.
        """
        self.add_option(label=yes_label, value="yes")
        self.add_option(label=no_label, value="no")
