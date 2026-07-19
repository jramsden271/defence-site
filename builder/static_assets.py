"""
Copies a hand-authored static asset (CSS, JS, images, ...) into ``dist/``
at build time. ``dist/`` is pure build output — nothing should be authored
directly inside it — so every CSS/JS/image file has a source location
under ``pages/shared/`` (used by more than one page) or under a specific
page's own folder (used by only that page), and gets copied into ``dist/``
from there.
"""

from pathlib import Path


def copy_static_asset(source_path: Path, dist_dir: Path, dest_relative_path: str) -> Path:
    """Copy ``source_path`` to ``dist_dir / dest_relative_path``, creating
    any needed directories. Returns the written path."""
    output_path = dist_dir / dest_relative_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(source_path.read_bytes())
    return output_path
