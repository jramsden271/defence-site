from pathlib import Path

from pydantic import Field

from builder.models.basic.html_tag import HtmlTag
from builder.models.basic.raw import Raw


class Page(HtmlTag):
    """
    A full, self-contained HTML document — the base for every buildable
    page on the site.

    Owns the shared ``<!DOCTYPE>``/``<head>``/``<body>`` skeleton (charset
    and viewport meta, favicon, shared CSS, the theme-init script, the
    shared :class:`~project.page_templates.shared.header.header.Header`
    and :class:`~project.page_templates.shared.footer.footer.Footer`) and
    wraps ``body`` in the ``page-content`` div common to every page. A
    page-specific subclass (e.g. a future ``DefenceGeneratorPage``) adds
    whatever else it needs — a form, page-specific assets, ... — and
    supplies its own ``title``/``body``/``head_extra`` here.

    :meth:`write` renders the page and writes it to
    ``dist_dir / f"{page_name}.html"``, replacing what every page's
    ``build_page.py`` used to do by hand (open a file, write the string,
    print a confirmation).
    """

    title: str = Field(..., description="The page's <title> text and its output filename stem.")
    page_name: str = Field(..., description="Output filename stem — written to dist_dir / f'{page_name}.html'.")
    body: list["str | HtmlTag"] = Field(default_factory=list, description="The page's own content.")
    head_extra: list["str | HtmlTag"] = Field(
        default_factory=list, description="Extra <head> markup (e.g. page-specific <link>/<script> tags)."
    )
    body_end_extra: list["str | HtmlTag"] = Field(
        default_factory=list,
        description="Extra markup placed after the shared footer but before </body>.",
    )

    def _shared_head(self) -> list["str | HtmlTag"]:
        """Boilerplate every page needs: charset/viewport meta, favicon,
        the site-wide shared CSS, and the theme-init script (must run
        synchronously, before first paint, so the page never flashes the
        wrong theme)."""
        from project.page_templates.shared.theme.build_theme import render_theme_init_script

        return [
            Raw(html='<meta charset="UTF-8">'),
            Raw(html='<meta name="viewport" content="width=device-width, initial-scale=1.0">'),
            Raw(html='<link rel="icon" type="image/x-icon" href="resources/car_icon_150909.ico">'),
            Raw(html='<link rel="stylesheet" href="css/colours.css">'),
            Raw(html='<link rel="stylesheet" href="css/style.css">'),
            Raw(html='<script src="js/theme.js" defer></script>'),
            Raw(html=render_theme_init_script()),
        ]

    def to_html(self) -> str:
        """Render the full document: ``<!DOCTYPE html>`` followed by
        ``<html>`` containing the shared head boilerplate + ``head_extra``
        + ``<title>``, then the shared header, ``body`` wrapped in
        ``page-content``, the shared footer, and ``body_end_extra``."""
        from project.page_templates.shared.footer.footer import Footer
        from project.page_templates.shared.header.header import Header

        head_children = [*self._shared_head(), *self.head_extra, Raw(html=f"<title>{self.title}</title>")]
        head_html = "\n".join(child.to_html() for child in head_children)

        page_content_html = "\n".join(
            child if isinstance(child, str) else child.to_html() for child in self.body
        )

        body_children: list[str | HtmlTag] = [
            Header(),
            Raw(html=f'<div class="page-content">\n{page_content_html}\n</div>'),
            Footer(),
            *self.body_end_extra,
        ]
        body_html = "\n".join(
            child if isinstance(child, str) else child.to_html() for child in body_children
        )

        return (
            "<!DOCTYPE html>\n"
            f"<html lang=\"en\">\n<head>\n{head_html}\n</head>\n<body>\n{body_html}\n</body>\n</html>\n"
        )

    def write(self, dist_dir: Path) -> Path:
        """Render this page and write it to
        ``dist_dir / f"{page_name}.html"``. Returns the written path."""
        dist_dir.mkdir(parents=True, exist_ok=True)
        output_path = dist_dir / f"{self.page_name}.html"
        output_path.write_text(self.to_html(), encoding="utf-8")
        print(f"Wrote {output_path}")
        return output_path
