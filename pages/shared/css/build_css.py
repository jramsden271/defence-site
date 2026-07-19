"""
Copies the site-wide shared CSS (used by every page) into ``dist/css/``.

Usage from the top-level build (``builder/build_everything.py``)::

    from pages.shared.css.build_css import write_shared_css

    write_shared_css(dist_dir)
"""

from pathlib import Path

from builder.static_assets import copy_static_asset

MODULE_DIR = Path(__file__).parent


def write_shared_css(dist_dir: Path) -> None:
    """Copy every ``.css`` file in this folder into ``dist/css/``. Add a new
    shared CSS file here and it's picked up automatically — no list to update."""
    for source_path in sorted(MODULE_DIR.glob("*.css")):
        copy_static_asset(source_path, dist_dir, f"css/{source_path.name}")
