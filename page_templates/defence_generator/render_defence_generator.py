"""
The ``defence_generator`` template: a ``content`` page built around a
question-and-answer form that generates defence text — an intro, a form,
and an output box (PoFA result line, generated paragraphs, character count,
copy-to-clipboard button).

Composes with ``content`` (calls :func:`render_content` for the outer page
skeleton) rather than subclassing it — the same "call into the next
template down, passing your own content" shape ``content`` itself uses for
header/footer.

A defence-generator page's own ``build_page.py`` supplies only what's
actually specific to that page: its questions (a ``Form`` built from
``builder.models.forms.*``), its intro copy, its own JS (the
``generate_text.js`` equivalent) and, optionally, extra page-specific
``<head>`` markup (e.g. if it needs ``pofa_date.js``). Everything common to
every defence-generator page — the output box markup, the radio-button
styling, the copy-to-clipboard/conditional-visibility wiring, and the
generated field manifest (``form_variables.js``) — is handled here, once,
so no page has to repeat it.

Usage from a page's ``build_page.py``::

    from page_templates.defence_generator.render_defence_generator import (
        render_defence_generator,
    )

    html = render_defence_generator(
        title="No stopping defence generator",
        page_name="no_stopping_defence",
        intro_html=intro_html,
        form=form,
        dist_dir=dist_dir,
        page_js_files=[page_dir / "js" / "generate_text.js"],
        extra_head="<script src=\"js/pofa_date.js\" defer></script>",
    )
"""

from pathlib import Path

from builder.field_manifest import write_manifest
from builder.models.forms.form import Form
from builder.static_assets import copy_static_asset
from page_templates.content.render_content import render_content

TEMPLATE_DIR = Path(__file__).parent


def _read(name: str) -> str:
    return (TEMPLATE_DIR / "blocks" / name).read_text(encoding="utf-8")


def render_defence_generator(
    title: str,
    page_name: str,
    intro_html: str,
    form: Form,
    dist_dir: Path,
    page_js_files: list[Path] = [],
    extra_head: str = "",
) -> str:
    """Assemble a full defence-generator page and write its generated
    assets (field manifest, template-owned CSS/JS) into ``dist_dir``.

    :param title: The page's ``<title>`` text.
    :param page_name: The page's slug, used for its page-specific resource
        path (``dist/resources/<page_name>/js/...``) — matches the page's
        own folder name under ``pages/``.
    :param intro_html: The page's intro copy, placed above the form.
    :param form: The page's :class:`Form`, used both to render the form
        itself and to generate ``form_variables.js``.
    :param dist_dir: The site's ``dist/`` directory.
    :param page_js_files: The page's own JS files (e.g. its
        ``generate_text.js``), copied into
        ``dist/resources/<page_name>/js/``.
    :param extra_head: Extra ``<head>`` markup the page needs beyond what
        every defence-generator page already gets (e.g. a
        ``<script src="js/pofa_date.js">`` tag, for pages that need PoFA
        date logic).
    """
    copy_static_asset(TEMPLATE_DIR / "css" / "radio.css", dist_dir, "css/radio.css")

    page_resources_dir = dist_dir / "resources" / page_name
    for js_file in page_js_files:
        copy_static_asset(js_file, dist_dir, f"resources/{page_name}/js/{js_file.name}")

    manifest_path = page_resources_dir / "js" / "form_variables.js"
    write_manifest(form, manifest_path)
    print(f"Wrote {manifest_path}")

    page_js_tags = "\n".join(
        f'    <script src="resources/{page_name}/js/{js_file.name}" defer></script>'
        for js_file in page_js_files
    )

    head_extra_lines = [
        '    <link rel="stylesheet" href="css/radio.css">',
        '    <script src="js/copy_to_clipboard.js" defer></script>',
        '    <script src="js/conditional_visibility.js" defer></script>',
    ]
    if extra_head:
        head_extra_lines.append(extra_head)
    head_extra_lines.append(
        f'    <script src="resources/{page_name}/js/form_variables.js" defer></script>'
    )
    if page_js_tags:
        head_extra_lines.append(page_js_tags)
    head_extra = "\n".join(head_extra_lines)

    body_html = "\n".join([
        intro_html,
        form.to_html(),
        _read("output_box.html"),
    ])

    return render_content(
        title=title,
        body_html=body_html,
        head_extra=head_extra,
    )
