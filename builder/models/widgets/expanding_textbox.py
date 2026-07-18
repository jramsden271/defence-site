from pydantic import Field

from models.basic.base_element import BaseElement
from models.basic.p import P


class ExpandingTextbox(BaseElement):
    """
    A collapsible ``<details>`` help block: a clickable ``summary`` that reveals
    one or more help paragraphs.
    """

    title: str = Field(
        default="Help", description="The clickable summary/heading text."
    )
    body: list[str]|str = Field(
        ..., description="Help paragraphs shown when the block is expanded."
    )

    def to_html(self) -> str:
        if isinstance(self.body, str):
            self.body = [self.body]
        inner = "\n".join(P(text=text).to_html() for text in self.body)
        return (
            "<details>\n"
            f"<summary>{self.title}</summary>\n"
            '<div class="help-content">\n'
            f"{inner}\n"
            "</div>\n"
            "</details>"
        )
