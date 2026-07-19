"""
Copies the site-wide shared resources (favicon, ...) into ``dist/resources/``.

Usage from the top-level build (``builder/build_everything.py``)::

    from pages.shared.resources.build_resources import write_shared_resources

    write_shared_resources(dist_dir)
"""

from pathlib import Path

from builder.static_assets import copy_static_asset

MODULE_DIR = Path(__file__).parent

_FILES = ["car_icon_150909.ico"]


def write_shared_resources(dist_dir: Path) -> None:
    """Copy every shared resource file into ``dist/resources/``."""
    for name in _FILES:
        copy_static_asset(MODULE_DIR / name, dist_dir, f"resources/{name}")
