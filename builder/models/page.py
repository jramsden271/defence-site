from pathlib import Path

from pydantic import Field

from builder.models.basic.html_tag import HtmlTag
from builder.models.basic.raw import Raw
from builder.models.component import Component
from builder.models.resource import ResourceBundle


class PageComponent(Component):
    """
    A full, self-contained HTML document — the base for every buildable
    page on the site.

    Owns the shared ``<!DOCTYPE>``/``<head>``/``<body>`` skeleton
    (charset and viewport meta, the shared
    :class:`~project.components.header.header.Header` and
    :class:`~project.components.footer.footer.Footer`) and wraps
    ``body`` in the ``page-content`` div common to every page. A
    page-specific subclass (e.g. ``DefenceGeneratorPage``) adds whatever
    else it needs — a form, page-specific assets, ... — and supplies its
    own ``title``/``body``/``head_extra`` here.

    A ``PageComponent`` is itself a :class:`Component`: its CSS/JS/media
    and any raw ``<head>`` markup (e.g. an inline pre-paint script) are
    whatever :meth:`gather_resources`/:meth:`gather_head_markup` collect
    from the shared ``Header``/``Footer`` and anything nested in
    ``body``/``head_extra``/``body_end_extra`` — there's no separate,
    hand-maintained list of "shared assets" to keep in sync.

    :meth:`write` renders the page and writes the ``.html`` file for a
    given site URL under ``dist_dir``. It does not write CSS/JS/media —
    see :meth:`~builder.build_everything.View.write_page`.
    """

    title: str = Field(..., description="The page's <title> text.")
    page_name: str = Field(
        ..., description="Short identifying name for the page (e.g. used to namespace its own resources)."
    )
    body: list["str | HtmlTag"] = Field(default_factory=list, description="The page's own content.")
    head_extra: list["str | HtmlTag"] = Field(
        default_factory=list, description="Extra <head> markup (e.g. page-specific <link>/<script> tags)."
    )
    body_end_extra: list["str | HtmlTag"] = Field(
        default_factory=list,
        description="Extra markup placed after the shared footer but before </body>.",
    )

    def _shared_components(self) -> "tuple[Component, Component]":
        """The Header/Footer components every page shares. A method
        (not fields with default factories) so the imports stay lazy,
        avoiding an import cycle with ``project.components``."""
        from project.components.footer.footer import Footer
        from project.components.header.header import Header

        return Header(), Footer()

    def _nested_components(self) -> list[Component]:
        header, footer = self._shared_components()
        return [
            header,
            footer,
            *(child for child in self.body if isinstance(child, Component)),
            *(child for child in self.head_extra if isinstance(child, Component)),
            *(child for child in self.body_end_extra if isinstance(child, Component)),
        ]

    def _shared_head(self) -> list["str | HtmlTag"]:
        """Boilerplate every page needs: charset/viewport meta."""
        return [
            Raw(html='<meta charset="UTF-8">'),
            Raw(html='<meta name="viewport" content="width=device-width, initial-scale=1.0">'),
        ]

    def _resource_tags(self, bundle: ResourceBundle, url_path: str) -> list["str | HtmlTag"]:
        """``<link>``/``<script>`` tags referencing the CSS/JS/media
        this page's ``bundle`` will be compiled into by
        :meth:`~builder.build_everything.View.write_page` — one
        ``{url_path}.css`` and one ``{url_path}.js`` beside the page's
        own ``.html``, plus a favicon ``<link>`` under ``resources/`` if
        a matching media resource (``*.ico``) was gathered."""
        tags: list[str | HtmlTag] = []
        for resource in bundle.media:
            if resource.resolved_dest_name().endswith(".ico"):
                tags.append(
                    Raw(
                        html=f'<link rel="icon" type="image/x-icon" '
                        f'href="resources/{resource.resolved_dest_name()}">'
                    )
                )
        if bundle.css:
            tags.append(Raw(html=f'<link rel="stylesheet" href="{url_path}.css">'))
        if bundle.js:
            tags.append(Raw(html=f'<script src="{url_path}.js" defer></script>'))
        return tags

    def to_html(self, url: str = "/") -> str:
        """Render the full document: ``<!DOCTYPE html>`` followed by
        ``<html>`` containing the shared head boilerplate + gathered
        resource tags + ``head_extra`` + ``<title>``, then the shared
        header, ``body`` wrapped in ``page-content``, the shared footer,
        and ``body_end_extra``. ``url`` is only used to name the
        CSS/JS ``<link>``/``<script>`` tags (see :meth:`_resource_tags`)
        — resolving the page's actual output location is
        :meth:`write`'s job."""
        header, footer = self._shared_components()
        bundle = self.gather_resources()

        head_children = [
            *self._shared_head(),
            *(Raw(html=html) for html in self.gather_head_markup()),
            *self._resource_tags(bundle, self.url_path(url)),
            *self.head_extra,
            Raw(html=f"<title>{self.title}</title>"),
        ]
        head_html = "\n".join(child.to_html() for child in head_children)

        page_content_html = "\n".join(
            child if isinstance(child, str) else child.to_html() for child in self.body
        )

        body_children: list[str | HtmlTag] = [
            header,
            Raw(html=f'<div class="page-content">\n{page_content_html}\n</div>'),
            footer,
            *self.body_end_extra,
        ]
        body_html = "\n".join(
            child if isinstance(child, str) else child.to_html() for child in body_children
        )

        return (
            "<!DOCTYPE html>\n"
            f"<html lang=\"en\">\n<head>\n{head_html}\n</head>\n<body>\n{body_html}\n</body>\n</html>\n"
        )

    def write(self, dist_dir: Path, url: str = "/") -> Path:
        """Render this page and write it to the ``.html`` file for
        ``url`` under ``dist_dir``. Does *not* write any CSS/JS/media —
        gathering and writing a page's resources is
        :class:`~builder.build_everything.View`'s job (see
        :meth:`gather_resources`), since only ``View`` knows the final
        per-URL/shared-media file layout. Returns the written path."""
        url_path = self.url_path(url)
        output_path = dist_dir / f"{url_path}.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_html(url), encoding="utf-8")
        print(f"Wrote {output_path}")
        return output_path

    @staticmethod
    def url_path(url: str) -> str:
        """Normalise a site-relative ``url`` (e.g. ``"/"``,
        ``"no-stopping-defence"``, ``"blog/news"``) to the
        slash-separated path its output should live at, relative to
        ``dist_dir`` and without a trailing ``.html``. The root path
        (``"/"`` or ``""``) becomes ``"index"``."""
        stripped = url.strip("/")
        return stripped if stripped else "index"
