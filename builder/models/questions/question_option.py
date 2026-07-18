from pydantic import BaseModel, ConfigDict, Field


class QuestionOption(BaseModel):
    """
    One possible answer to a :class:`~models.questions.multiple_choice_question.MultipleChoiceQuestion`.

    Pure data — label, value and optional description. Rendering it as HTML
    (e.g. as a radio button) is the responsibility of the control that owns
    the question.
    """

    model_config = ConfigDict(extra="forbid")

    label: str = Field(..., description="The option's display label.")
    value: str = Field(..., description="The value associated with the option.")
    description: str = Field(
        default="", description="Optional description text for the option."
    )
