from pydantic import BaseModel, ConfigDict, Field


class BaseQuestion(BaseModel):
    """
    Base class for all questions: plain data describing what's being asked,
    with no knowledge of how it will be rendered as HTML.

    Help text is recorded as plain ``help_title``/``help_body`` strings; it's
    up to the control rendering the question to turn that into whatever
    widget it uses (e.g. an ``ExpandingTextbox``) — see
    :func:`~models.basic.base_element.render_help`.
    """

    model_config = ConfigDict(extra="forbid")

    display_question: str = Field(..., description="The question text.")
    help_title: str | None = Field(
        default=None, description="Title/summary for the help block, if any."
    )
    help_body: list[str] = Field(
        default_factory=list, description="Help paragraphs; empty means no help."
    )

    def add_help(self, title: str | None = None, body: list[str] | str | None = None) -> None:
        """Set this question's help text."""
        if isinstance(body, str):
            body = [body]
        self.help_title = title
        self.help_body = list(body or [])
