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

PAGE_BUILDERS = [
    repo_root / "pages" / "index" / "build_page.py",
    repo_root / "pages" / "no_stopping_defence" / "build_page.py",
]

for page_builder in PAGE_BUILDERS:
    print(f"--- Building {page_builder.relative_to(repo_root)} ---")
    runpy.run_path(str(page_builder), run_name="__main__")
