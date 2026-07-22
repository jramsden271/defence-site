from typing import ClassVar

from builder.models.basic.html_tag import Conditional


class Nav(Conditional):
    """
    A ``<nav>`` element. ``children`` is its content.
    """

    tag: ClassVar[str] = "nav"
