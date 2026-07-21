from pathlib import Path

from pydantic import Field

from builder.field_manifest import write_manifest
from builder.models.basic.html_tag import HtmlTag
from builder.models.basic.raw import Raw
from builder.models.forms.form import Form
from builder.models.page import Page
from builder.static_assets import copy_static_asset

TEMPLATE_DIR = Path(__file__).parent


def _read_block(name: str) -> str:
    return (TEMPLATE_DIR / "blocks" / name).read_text(encoding="utf-8")


class DefenceGeneratorPage(Page):
    """
    A ``content`` page (see :class:`~builder.models.page.Page`) built
    around a question-and-answer form that generates defence text — an
    intro, a form, and an output box (PoFA result line, generated
    paragraphs, character count, copy-to-clipboard button).

    A defence-generator page's own ``build_page.py`` supplies only what's
    actually specific to that page: its questions (``form``), its intro
    copy, its own JS/CSS (authored under its own ``js/``/``css/``
    folders — every file there is picked up automatically, no list to
    maintain), and ``page_dir``/``page_name`` (see :class:`Page`).
    Everything common to every defence-generator page — the output box
    markup, the radio-button styling, the copy-to-clipboard/conditional-
    visibility/PoFA-date wiring, and the generated field manifest
    (``form_variables.js``) — is handled here, once, so no page has to
    repeat it. Add a new template-wide JS/CSS file under this class's own
    folder's ``js/``/``css/`` and it's picked up automatically too, same
    as a page's own assets.

    Usage from a page's ``build_page.py``::

        from project.page_templates.defence_generator.defence_generator_page import (
            DefenceGeneratorPage,
        )

        page = DefenceGeneratorPage(
            title="No stopping defence generator",
            page_name="no_stopping_defence",
            intro_html=intro_html,
            form=form,
            page_dir=page_dir,
        )
        page.write(dist_dir)
    """

    form: Form = Field(..., description="The page's question-and-answer form.")
    intro_html: str = Field(..., description="The page's intro copy, placed above the form.")
    page_dir: Path = Field(
        ..., description="The page's own folder, for globbing its js/css assets."
    )

    def write(self, dist_dir: Path) -> Path:
        """As :meth:`Page.write`, but first writes this template's own and
        this page's own CSS/JS assets, plus the generated field manifest
        (``form_variables.js``), and builds ``head_extra`` to reference
        them all."""
        copy_static_asset(TEMPLATE_DIR / "css" / "radio.css", dist_dir, "css/radio.css")

        template_js_files = sorted((TEMPLATE_DIR / "js").glob("*.js"))
        for js_file in template_js_files:
            copy_static_asset(js_file, dist_dir, f"js/{js_file.name}")

        page_resources_dir = dist_dir / "resources" / self.page_name

        page_js_files = sorted((self.page_dir / "js").glob("*.js"))
        for js_file in page_js_files:
            copy_static_asset(js_file, dist_dir, f"resources/{self.page_name}/js/{js_file.name}")

        page_css_files = sorted((self.page_dir / "css").glob("*.css"))
        for css_file in page_css_files:
            copy_static_asset(css_file, dist_dir, f"resources/{self.page_name}/css/{css_file.name}")

        manifest_path = page_resources_dir / "js" / "form_variables.js"
        write_manifest(self.form, manifest_path)
        print(f"Wrote {manifest_path}")

        head_extra: list[str | HtmlTag] = [Raw(html='<link rel="stylesheet" href="css/radio.css">')]
        for css_file in page_css_files:
            head_extra.append(
                Raw(html=f'<link rel="stylesheet" href="resources/{self.page_name}/css/{css_file.name}">')
            )
        head_extra += [
            Raw(html='<script src="js/copy_to_clipboard.js" defer></script>'),
            Raw(html='<script src="js/conditional_visibility.js" defer></script>'),
            Raw(html='<script src="js/pofa_date.js" defer></script>'),
        ]
        for js_file in template_js_files:
            head_extra.append(Raw(html=f'<script src="js/{js_file.name}" defer></script>'))
        head_extra.append(
            Raw(html=f'<script src="resources/{self.page_name}/js/form_variables.js" defer></script>')
        )
        for js_file in page_js_files:
            head_extra.append(
                Raw(html=f'<script src="resources/{self.page_name}/js/{js_file.name}" defer></script>')
            )

        self.head_extra = head_extra
        self.body = [Raw(html=self.intro_html), self.form, Raw(html=_read_block("output_box.html"))]

        return super().write(dist_dir)
