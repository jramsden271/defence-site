from pathlib import Path
from typing import ClassVar

from pydantic import Field

from builder.field_manifest import render_manifest
from builder.models.basic.html_tag import HtmlTag
from builder.models.component import Component
from builder.models.forms.form import Form
from builder.models.page import PageComponent
from builder.models.resource import Resource, ResourceBundle
from project.page_components.defence_generator.components.output_box import OutputBox
from project.page_components.shared.shared_assets import SharedAssets

TEMPLATE_DIR = Path(__file__).parent


def _page_own_assets(page_dir: Path) -> Component:
    """The page's own ``css/``/``js/`` folders (under ``page_dir``), as
    a nested component — every file there is picked up automatically,
    same convention as any other component's ``css_dir``/``js_dir``."""
    return Component(
        resources=ResourceBundle(
            css=[Resource(source_path=path) for path in sorted((page_dir / "css").glob("*.css"))],
            js=[Resource(source_path=path) for path in sorted((page_dir / "js").glob("*.js"))],
        )
    )


class DefenceGeneratorPage(PageComponent):
    """
    A :class:`~builder.models.page.PageComponent` built around a
    question-and-answer form that generates defence text — an intro, a
    form, and an output box (PoFA result line, generated paragraphs,
    character count, copy-to-clipboard button).

    A defence-generator page's own ``build_page.py`` supplies only what's
    actually specific to that page: its questions (``form``), its intro
    copy (an ``HtmlTag``/:class:`Component` — e.g. a page-local
    ``Intro`` component under that page's own ``components/`` folder,
    not raw HTML), its own JS/CSS (authored under its own ``js/``/``css/``
    folders — every file there is picked up automatically, no list to
    maintain), and ``page_dir``/``page_name`` (see :class:`PageComponent`).
    Everything common to every defence-generator page — the output box
    markup, the radio-button styling (this class's own ``css/``/``js/``
    folders), and the generated field manifest (``form_variables.js``,
    built fresh from ``form`` on every render) — is handled here, once,
    so no page has to repeat it.

    Usage from a page's ``build_page.py``::

        from project.page_components.defence_generator.defence_generator_page import (
            DefenceGeneratorPage,
        )

        page = DefenceGeneratorPage(
            title="No stopping defence generator",
            page_name="no_stopping_defence",
            intro=Intro(),
            form=form,
            page_dir=page_dir,
        )
        page.write(dist_dir, url="no-stopping-defence")
    """

    css_dir: ClassVar[Path | None] = TEMPLATE_DIR / "css"
    js_dir: ClassVar[Path | None] = TEMPLATE_DIR / "js"

    form: Form = Field(..., description="The page's question-and-answer form.")
    intro: HtmlTag = Field(..., description="The page's intro copy, placed above the form.")
    page_dir: Path = Field(
        ..., description="The page's own folder, for globbing its js/css assets."
    )

    def _nested_components(self) -> list[Component]:
        manifest = Component(
            resources=ResourceBundle(
                js=[Resource(content=render_manifest(self.form), dest_name="form_variables.js")]
            )
        )
        nested = [*super()._nested_components(), SharedAssets(), _page_own_assets(self.page_dir), manifest]
        if isinstance(self.intro, Component):
            nested.append(self.intro)
        return nested

    def to_html(self, url: str = "/") -> str:
        self.body = [self.intro, self.form, OutputBox()]
        return super().to_html(url)
