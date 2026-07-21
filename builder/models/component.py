from builder.models.basic.html_tag import HtmlTag


class Component(HtmlTag):
    """
    Marker base class for a reusable page fragment (e.g. the site header,
    footer, or a page template's output box) — as opposed to a raw
    structural tag like :class:`~models.basic.div.Div`.

    Adds no fields or behaviour of its own beyond :class:`HtmlTag`; it
    exists so a fragment meant to be composed into a page can be written
    as a named class (``class Header(Component): ...``) rather than a
    free ``render_*()`` function reading a ``.html`` file.
    """
