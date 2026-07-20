from typing import ClassVar

from builder.models.basic.html_tag import Conditional


class H1(Conditional):
    """A ``<h1>`` heading. ``elements`` is the heading's content."""

    tag: ClassVar[str] = "h1"


class H2(Conditional):
    """A ``<h2>`` heading. ``elements`` is the heading's content."""

    tag: ClassVar[str] = "h2"


class H3(Conditional):
    """A ``<h3>`` heading. ``elements`` is the heading's content."""

    tag: ClassVar[str] = "h3"


class H4(Conditional):
    """A ``<h4>`` heading. ``elements`` is the heading's content."""

    tag: ClassVar[str] = "h4"


class H5(Conditional):
    """A ``<h5>`` heading. ``elements`` is the heading's content."""

    tag: ClassVar[str] = "h5"


class H6(Conditional):
    """A ``<h6>`` heading. ``elements`` is the heading's content."""

    tag: ClassVar[str] = "h6"
