from pathlib import Path
from typing import ClassVar

from builder.models.component import Component

SHARED_DIR = Path(__file__).parent


class SharedAssets(Component):
    """
    Assets shared by every page-component that includes it: the
    colour-variable/layout stylesheets (``colours.css``, ``style.css``),
    the favicon, the dark/light theme mechanism (the toggle button's
    deferred click-handler script, ``theme.js``, plus the synchronous
    pre-paint ``<head>`` snippet that sets ``data-theme`` before first
    paint — see :meth:`_own_head_markup` — so the page never flashes
    the wrong theme), and the other plain (no per-page templating)
    shared scripts (``conditional_visibility.js``, ``copy_to_clipboard.js``,
    ``pofa_date.js``). Contributes no visible body markup of its own —
    it exists purely so a page-component (e.g.
    :class:`~project.page_components.content.content_page.ContentPage`,
    :class:`~project.page_components.defence_generator.defence_generator_page.DefenceGeneratorPage`)
    can pick these up via
    :meth:`~builder.models.component.Component.gather_resources` by
    including this component, rather than every page getting them
    unconditionally.
    """

    css_dir: ClassVar[Path | None] = SHARED_DIR / "css"
    js_dir: ClassVar[Path | None] = SHARED_DIR / "js"
    media_dir: ClassVar[Path | None] = SHARED_DIR / "resources"

    def _own_head_markup(self) -> list[str]:
        """The inline pre-paint theme-init script: must run
        synchronously in ``<head>`` (not deferred, unlike ``theme.js``),
        since it runs before ``<body>`` exists — reading a saved
        preference from ``localStorage`` or falling back to the
        OS/browser's ``prefers-color-scheme``."""
        script_path = SHARED_DIR / "theme_init.html"
        return [script_path.read_text(encoding="utf-8")]
