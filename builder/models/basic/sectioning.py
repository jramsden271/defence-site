from typing import ClassVar

from builder.models.basic.html_tag import Conditional


class Header(Conditional):
    """
    A ``<header>`` element. ``children`` is its content.
    """

    tag: ClassVar[str] = "header"


class Footer(Conditional):
    """
    A ``<footer>`` element. ``children`` is its content.
    """

    tag: ClassVar[str] = "footer"
