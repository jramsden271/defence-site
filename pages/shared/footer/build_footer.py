"""
Builds the shared site footer, for other pages to inject into their own
output.

Usage from another page's ``build_page.py``::

    from pages.shared.footer.build_footer import render_footer

    html += render_footer()
"""

from pathlib import Path

FOOTER_DIR = Path(__file__).parent


def render_footer() -> str:
    """Return the shared ``<footer>`` block's HTML."""
    footer_path = FOOTER_DIR / "layout" / "footer.html"
    return footer_path.read_text(encoding="utf-8")
