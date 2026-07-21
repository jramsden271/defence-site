"""
Builds the shared site header, for templates to inject into their own
output.

Usage from a template's render module::

    from project.page_templates.shared.header.build_header import render_header

    html += render_header()
"""

from pathlib import Path

HEADER_DIR = Path(__file__).parent


def render_header() -> str:
    """Return the shared ``<header>`` block's HTML."""
    header_path = HEADER_DIR / "layout" / "header.html"
    return header_path.read_text(encoding="utf-8")
