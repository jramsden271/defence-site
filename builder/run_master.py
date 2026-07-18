"""
Entry point for building the website.

Run from anywhere:

    python builder/run_master.py

Builds every page by running each page's ``run_builder.py``. Currently
there's just the one page; as more are added, this is where they all get
built from.
"""

import runpy
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent

# run_builder.py files import from the `builder` package via absolute
# imports (e.g. `from builder.models.basic.div import Div`), so the repo
# root — not `builder/` itself — needs to be on sys.path for those to resolve.
sys.path.insert(0, str(repo_root))

PAGE_BUILDERS = [
    repo_root / "pages" / "no_stopping_defence" / "run_builder.py",
]

for page_builder in PAGE_BUILDERS:
    print(f"--- Building {page_builder.relative_to(repo_root)} ---")
    runpy.run_path(str(page_builder), run_name="__main__")
