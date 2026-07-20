from pydantic import BaseModel, ConfigDict, Field


class HelpText(BaseModel):
    """A question's help title/body, validated (e.g. when loaded from JSON)."""

    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default="Help", description="Title/summary for the help block, if any.")
    body: str = Field(default="", description="Help text; empty means no help.")


class BaseQuestion(BaseModel):
    """
    Base class for all questions: plain data describing what's being asked,
    with no knowledge of how it will be rendered as HTML.

    Help text is recorded as a :class:`HelpText`; it's up to the control
    rendering the question to turn that into whatever widget it uses (e.g. an
    ``ExpandingTextbox``) — see :func:`~models.basic.html_tag.render_help`.
    """

    model_config = ConfigDict(extra="forbid")

    display_question: str = Field(..., description="The question text.")
    help: HelpText | None = Field(
        default=None, description="Help title/body for this question, if any."
    )

    def add_help(self, title: str | None = None, body: str = "") -> None:
        """Set this question's help text inline.

        Separate paragraphs in ``body`` with a blank line (``\\n\\n``).
        """
        self.help = HelpText(title=title, body=body)

    def set_help(self, help_text: HelpText|str) -> None:
        """Set this question's help text from an existing :class:`HelpText`
        (e.g. one loaded from a page's ``help_text.json``)."""
        if isinstance(help_text, str):
            self.help = HelpText(body=help_text)
        else:
            self.help = help_text
