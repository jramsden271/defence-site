"""
The ``content`` template: the base page type every other template composes
with. Provides the ``<html>``/``<head>`` boilerplate, the shared header and
footer, and a ``page-content`` wrapper, common to every page on the site.

A page (or a more specific template, e.g. ``defence_generator``) supplies
only its own content (page title, any extra ``<head>`` tags it needs, its
body HTML, and — if it has JS that must run after the footer — a closing
script block), then calls :func:`render_content` to assemble the full
document. This way, no page can forget the header/footer, get the skeleton's
tags mismatched, or diverge in shared boilerplate (favicon, shared CSS,
viewport meta, ...).

Usage from a page's ``build_page.py`` (or a template built on top of this
one)::

    from page_templates.content.render_content import render_content

    html = render_content(
        title="My Page",
        head_extra='<script src="resources/my_page/js/thing.js" defer></script>',
        body_html="<h2>My Page</h2><p>...</p>",
    )
"""

from page_templates.shared.footer.build_footer import render_footer
from page_templates.shared.header.build_header import render_header
from page_templates.shared.theme.build_theme import render_theme_init_script

# Boilerplate every page needs: charset/viewport meta, favicon, the
# site-wide shared CSS, and the theme-init script (must run synchronously,
# before first paint, so the page never flashes the wrong theme — see
# render_theme_init_script's docstring). Page-specific <head> additions
# (title, extra stylesheets/scripts) are passed in via `head_extra`.
_SHARED_HEAD = f"""\
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="resources/car_icon_150909.ico">
    <link rel="stylesheet" href="css/colours.css">
    <link rel="stylesheet" href="css/style.css">
    <script src="js/theme.js" defer></script>
{render_theme_init_script()}"""


def render_content(
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
