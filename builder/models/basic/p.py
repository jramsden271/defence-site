from typing import ClassVar

from builder.models.basic.html_tag import Conditional
from builder.models.basic.raw import Raw


class P(Conditional):
    """
    Represents a paragraph element in the model.
    """

    tag: ClassVar[str] = "p"

    @classmethod
    def from_text(cls, text: str):
        """``text`` may contain inline HTML (e.g. ``<em>``), which is emitted as-is."""
        return cls(children=[Raw.from_text(text)])
