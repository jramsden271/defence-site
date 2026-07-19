"""
Copies the shared PoFA (Protection of Freedoms Act) date-calculation logic
into ``dist/js/``. Used by any page that needs to work out whether a Notice
to Keeper was issued in time.

Usage from the top-level build (``builder/build_everything.py``)::

    from pages.shared.pofa_date.build_pofa_date import write_pofa_date_js

    write_pofa_date_js(dist_dir)
"""

from pathlib import Path

from builder.static_assets import copy_static_asset

MODULE_DIR = Path(__file__).parent


def write_pofa_date_js(dist_dir: Path) -> Path:
    """Copy the shared ``pofa_date.js`` into ``dist/js/``. Returns the
    written path."""
    return copy_static_asset(MODULE_DIR / "pofa_date.js", dist_dir, "js/pofa_date.js")
