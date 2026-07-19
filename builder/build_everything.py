"""
Entry point for building the website.

Run from anywhere:

    python builder/build_everything.py

Builds every page by running each page's ``build_page.py``. Add a new
page's ``build_page.py`` to ``PAGE_BUILDERS`` below to include it.
"""

import runpy
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent

# build_page.py files import from the `builder` package via absolute
# imports (e.g. `from builder.models.basic.div import Div`), so the repo
# root — not `builder/` itself — needs to be on sys.path for those to resolve.
sys.path.insert(0, str(repo_root))

from page_templates.shared.css.build_css import write_shared_css  # noqa: E402
from page_templates.shared.js.build_js import write_shared_js  # noqa: E402
from page_templates.shared.resources.build_resources import write_shared_resources  # noqa: E402
from page_templates.shared.theme.build_theme import write_theme_js  # noqa: E402

dist_dir = repo_root / "dist"

# Shared assets used by every page, written once here rather than by each
# page's own build_page.py.
write_shared_css(dist_dir)
write_shared_resources(dist_dir)
write_theme_js(dist_dir)
write_shared_js(dist_dir)

PAGE_BUILDERS = [
    repo_root / "pages" / "index" / "build_page.py",
    repo_root / "pages" / "no_stopping_defence" / "build_page.py",
]

for page_builder in PAGE_BUILDERS:
    print(f"--- Building {page_builder.relative_to(repo_root)} ---")
    runpy.run_path(str(page_builder), run_name="__main__")
