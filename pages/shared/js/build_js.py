"""
Copies the shared JS files that are simply copied as-is (no per-page
templating) into ``dist/js/``.

Usage from the top-level build (``builder/build_everything.py``)::

    from pages.shared.js.build_js import write_shared_js

    write_shared_js(dist_dir)
"""

from pathlib import Path

from builder.static_assets import copy_static_asset

MODULE_DIR = Path(__file__).parent


def write_shared_js(dist_dir: Path) -> None:
    """Copy every ``.js`` file in this folder into ``dist/js/``. Add a new
    shared JS file here and it's picked up automatically — no list to update."""
    for source_path in sorted(MODULE_DIR.glob("*.js")):
        copy_static_asset(source_path, dist_dir, f"js/{source_path.name}")
