from typing import ClassVar

from builder.models.basic.html_tag import Conditional


class Em(Conditional):
    """
    Represents an emphasis element in the model.
    """

    tag: ClassVar[str] = "em"

    @classmethod
    def from_text(cls, text: str):
        """``text`` may contain inline HTML (e.g. ``<em>``), which is emitted as-is."""
        return cls(children=[text])
