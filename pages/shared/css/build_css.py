"""
Copies the site-wide shared CSS (used by every page) into ``dist/css/``.

Usage from the top-level build (``builder/build_everything.py``)::

    from pages.shared.css.build_css import write_shared_css

    write_shared_css(dist_dir)
"""

from pathlib import Path

from builder.static_assets import copy_static_asset

MODULE_DIR = Path(__file__).parent

_FILES = ["colours.css", "style.css"]


def write_shared_css(dist_dir: Path) -> None:
    """Copy every shared CSS file into ``dist/css/``."""
    for name in _FILES:
        copy_static_asset(MODULE_DIR / name, dist_dir, f"css/{name}")
