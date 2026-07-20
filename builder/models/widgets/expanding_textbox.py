from pydantic import Field

from builder.models.basic.html_tag import HtmlTag
from builder.models.basic.p import P


class ExpandingTextbox(HtmlTag):
    """
    A collapsible ``<details>`` help block: a clickable ``summary`` that reveals
    the help text.
    """

    title: str = Field(
        default="Help", description="The clickable summary/heading text."
    )
    body: str = Field(
        ..., description="Help text shown when the block is expanded. "
        "Separate paragraphs with a blank line (\\n\\n)."
    )

    def to_html(self) -> str:
        paragraphs = self.body.split("\n\n")
        inner = "\n".join(P(text=paragraph).to_html() for paragraph in paragraphs)
        return (
            "<details>\n"
            f"<summary>{self.title}</summary>\n"
            '<div class="help-content">\n'
            f"{inner}\n"
            "</div>\n"
            "</details>"
        )
