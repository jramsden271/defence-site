"""
Builds the shared dark/light theme assets: the inline pre-paint theme-init
script (embedded directly into every page's ``<head>``) and the deferred
``theme.js`` file (the toggle button's click behaviour), copied once into
``dist/js/``.

Usage from ``page_templates/content/render_content.py``::

    from project.page_templates.shared.theme.build_theme import render_theme_init_script

    head_extra = render_theme_init_script() + ...

And once, from the top-level build (``builder/build_everything.py``), to
place the shared ``theme.js`` file into ``dist/js/``::

    from project.page_templates.shared.theme.build_theme import write_theme_js

    write_theme_js(dist_dir)
"""

from pathlib import Path

THEME_DIR = Path(__file__).parent


def render_theme_init_script() -> str:
    """Return the inline ``<script>`` that sets ``data-theme`` on ``<html>``
    before first paint, so the page never flashes the wrong theme.

    Must run synchronously in ``<head>`` (not deferred) — it runs before
    ``<body>`` exists, reading a saved preference from ``localStorage`` or
    falling back to the OS/browser's ``prefers-color-scheme``.
    """
    script_path = THEME_DIR / "layout" / "theme_init.html"
    return script_path.read_text(encoding="utf-8")


def write_theme_js(dist_dir: Path) -> Path:
    """Copy the shared ``theme.js`` (toggle button behaviour) into
    ``dist/js/theme.js``. Returns the written path."""
    js_dir = dist_dir / "js"
    js_dir.mkdir(parents=True, exist_ok=True)
    output_path = js_dir / "theme.js"
    source = (THEME_DIR / "theme.js").read_text(encoding="utf-8")
    output_path.write_text(source, encoding="utf-8")
    return output_path
