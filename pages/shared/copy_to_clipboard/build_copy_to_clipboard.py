"""
Builds the shared clipboard-copy behaviour, copied once into ``dist/js/``.

Usage from the top-level build (``builder/build_everything.py``)::

    from pages.shared.copy_to_clipboard.build_copy_to_clipboard import write_copy_to_clipboard_js

    write_copy_to_clipboard_js(dist_dir)

A page that wants it includes ``<script src="js/copy_to_clipboard.js" defer></script>``
in its own ``head_extra`` and a button calling ``copyToClipboard()``.
"""

from pathlib import Path

MODULE_DIR = Path(__file__).parent


def write_copy_to_clipboard_js(dist_dir: Path) -> Path:
    """Copy the shared ``copy_to_clipboard.js`` into ``dist/js/``. Returns
    the written path."""
    js_dir = dist_dir / "js"
    js_dir.mkdir(parents=True, exist_ok=True)
    output_path = js_dir / "copy_to_clipboard.js"
    source = (MODULE_DIR / "copy_to_clipboard.js").read_text(encoding="utf-8")
    output_path.write_text(source, encoding="utf-8")
    return output_path
