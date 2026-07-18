"""
Builds the shared site header, for other pages to inject into their own
output.

Usage from another page's ``build_page.py``::

    from pages.shared.header.build_header import render_header

    html += render_header()
"""

from pathlib import Path

HEADER_DIR = Path(__file__).parent


def render_header() -> str:
    """Return the shared ``<header>`` block's HTML."""
    header_path = HEADER_DIR / "layout" / "header.html"
    return header_path.read_text(encoding="utf-8")
