"""
Builds the shared site footer, for templates to inject into their own
output.

Usage from a template's render module::

    from project.page_templates.shared.footer.build_footer import render_footer

    html += render_footer()
"""

from pathlib import Path

FOOTER_DIR = Path(__file__).parent


def render_footer() -> str:
    """Return the shared ``<footer>`` block's HTML."""
    footer_path = FOOTER_DIR / "layout" / "footer.html"
    return footer_path.read_text(encoding="utf-8")
