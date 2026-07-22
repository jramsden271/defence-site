"""
Entry point for building the website.

Run from anywhere:

    python builder/build_everything.py

Builds every page listed in ``views`` below. Each entry is a
:class:`View`, mapping a folder under ``project/pages/`` to the site URL
its page should be written to. Add a new page by adding its folder here.
"""

import runpy
import sys
from pathlib import Path

from pydantic import BaseModel

repo_root = Path(__file__).parent.parent

# build_page.py files import from the `builder` package via absolute
# imports (e.g. `from builder.models.basic.div import Div`), so the repo
# root — not `builder/` itself — needs to be on sys.path for those to resolve.
sys.path.insert(0, str(repo_root))

from builder.models.page import PageComponent  # noqa: E402

DIST_DIR = repo_root / "dist"


class View(BaseModel):
    """Maps a page folder under ``project/pages/`` to the site URL its
    page should be written to (e.g. ``dir="no_stopping_defence",
    url="no-stopping-defence"`` writes ``dist/no-stopping-defence.html``,
    ``dist/no-stopping-defence.css`` and ``dist/no-stopping-defence.js``,
    with any media shared via ``dist/resources/``).
    """

    dir: str
    url: str

    def get_page(self) -> PageComponent:
        """Import ``project/pages/{self.dir}/build_page.py`` and call
        its ``get_page()`` to obtain this view's :class:`PageComponent`."""
        build_page_path = repo_root / "project" / "pages" / self.dir / "build_page.py"
        if not build_page_path.is_file():
            raise FileNotFoundError(
                f"View(dir={self.dir!r}) has no build_page.py at {build_page_path}"
            )

        module = runpy.run_path(str(build_page_path), run_name=f"pages.{self.dir}.build_page")

        get_page = module.get("get_page")
        if get_page is None:
            raise AttributeError(
                f"{build_page_path} does not define a get_page() function"
            )

        return get_page()

    def write_page(self, dist_dir: Path = DIST_DIR) -> None:
        """Write this view's page and its resources: the ``.html`` file
        (:meth:`PageComponent.write`); its gathered CSS concatenated into one
        ``{url_path}.css`` and JS into one ``{url_path}.js``, both
        beside the ``.html``; and its gathered media files copied into
        the shared ``dist_dir / "resources"`` folder."""
        print(f"--- Building {self.dir} -> {self.url} ---")
        page = self.get_page()
        url_path = PageComponent.url_path(self.url)

        page.write(dist_dir, self.url)

        bundle = page.gather_resources()
        self._write_concatenated(bundle_resources=bundle.css, dist_dir=dist_dir, url_path=url_path, extension="css")
        self._write_concatenated(bundle_resources=bundle.js, dist_dir=dist_dir, url_path=url_path, extension="js")

        resources_dir = dist_dir / "resources"
        resources_dir.mkdir(parents=True, exist_ok=True)
        for resource in bundle.media:
            output_path = resources_dir / resource.resolved_dest_name()
            output_path.write_bytes(resource.read_bytes())

    @staticmethod
    def _write_concatenated(bundle_resources, dist_dir: Path, url_path: str, extension: str) -> None:
        if not bundle_resources:
            return
        output_path = dist_dir / f"{url_path}.{extension}"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        combined = "\n".join(resource.read_text() for resource in bundle_resources)
        output_path.write_text(combined, encoding="utf-8")
        print(f"Wrote {output_path}")


views = [
    View(dir="index", url="/"),
    View(dir="no_stopping_defence", url="no-stopping-defence"),
    View(dir="ntk_compliance_check", url="ntk-compliance-check"),
]

for view in views:
    view.write_page()
