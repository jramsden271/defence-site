"""
Shared page skeleton: the ``<html>``/``<head>`` boilerplate, the shared
header and footer, and the ``page-content`` wrapper, common to every page.

A page's own ``build_page.py`` builds only its own content (page title,
any extra ``<head>`` tags it needs, its body HTML, and — if it has
page-specific JS that must run after the footer — a closing script block),
then calls :func:`render_page` to assemble the full document. This way, no
page can forget the header/footer, get the skeleton's tags mismatched, or
diverge in shared boilerplate (favicon, shared CSS, viewport meta, ...).

Usage from a page's ``build_page.py``::

    from pages.shared.layout.render_page import render_page

    html = render_page(
        title="My Page",
        head_extra='<script src="resources/my_page/js/thing.js" defer></script>',
        body_html="<h2>My Page</h2><p>...</p>",
    )
"""

from pages.shared.footer.build_footer import render_footer
from pages.shared.header.build_header import render_header

# Boilerplate every page needs: charset/viewport meta, favicon, and the
# site-wide shared CSS. Page-specific <head> additions (title, extra
# stylesheets/scripts) are passed in via `head_extra`.
_SHARED_HEAD = """\
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="resources/car_icon_150909.ico">
    <link rel="stylesheet" href="css/colours.css">
    <link rel="stylesheet" href="css/style.css">"""


def render_page(
    title: str,
    body_html: str,
    head_extra: str = "",
    body_end_extra: str = "",
) -> str:
    """Assemble a full HTML document from a page's content.

    :param title: The page's ``<title>`` text.
    :param body_html: The page's own content, placed inside
        ``<div class="page-content">``.
    :param head_extra: Extra ``<head>`` markup (e.g. page-specific
        ``<link>``/``<script src>`` tags), placed after the shared head
        boilerplate.
    :param body_end_extra: Extra markup placed after the shared footer but
        before ``</body>`` (e.g. an inline ``<script>`` block a page needs
        to run, such as visibility-toggling logic).
    """
    head_extra_block = f"\n{head_extra}" if head_extra else ""
    body_end_block = f"\n{body_end_extra}" if body_end_extra else ""

    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
{_SHARED_HEAD}{head_extra_block}

    <title>{title}</title>
</head>
<body>

{render_header()}

<div class="page-content">

{body_html}

</div>

{render_footer()}{body_end_block}

</body>
</html>
"""
