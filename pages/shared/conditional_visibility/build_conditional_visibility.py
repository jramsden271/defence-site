"""
Builds the shared conditional-visibility behaviour (the ``data-trigger``/
``data-depends-on`` field-toggling logic), copied once into ``dist/js/``.

Usage from the top-level build (``builder/build_everything.py``)::

    from pages.shared.conditional_visibility.build_conditional_visibility import (
        write_conditional_visibility_js,
    )

    write_conditional_visibility_js(dist_dir)

A page that has conditional fields (via ``Triggerable``/``Conditional``
elements — see ``builder/models/basic/base_element.py``) includes
``<script src="js/conditional_visibility.js" defer></script>`` in its own
``head_extra``; no further wiring needed, it attaches to the whole document.
"""

from pathlib import Path

MODULE_DIR = Path(__file__).parent


def write_conditional_visibility_js(dist_dir: Path) -> Path:
    """Copy the shared ``conditional_visibility.js`` into ``dist/js/``.
    Returns the written path."""
    js_dir = dist_dir / "js"
    js_dir.mkdir(parents=True, exist_ok=True)
    output_path = js_dir / "conditional_visibility.js"
    source = (MODULE_DIR / "conditional_visibility.js").read_text(encoding="utf-8")
    output_path.write_text(source, encoding="utf-8")
    return output_path
