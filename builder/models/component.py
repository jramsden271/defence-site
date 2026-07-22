from pathlib import Path
from typing import ClassVar

from pydantic import Field

from builder.models.basic.html_tag import HtmlTag
from builder.models.resource import Resource, ResourceBundle


class Component(HtmlTag):
    """
    Base class for a reusable page fragment (e.g. the site header,
    footer, or a page template's output box) — as opposed to a raw
    structural tag like :class:`~models.basic.div.Div`.

    Beyond :class:`HtmlTag`, a ``Component`` is aware of the static
    assets *it* needs to function, categorised as ``css``/``js``/
    ``media``. A subclass declares these declaratively via three
    ``ClassVar`` folder paths — set whichever apply:

    - ``css_dir``: every ``*.css`` file directly in this folder is one
      of this component's stylesheets.
    - ``js_dir``: every ``*.js`` file directly in this folder is one of
      this component's scripts.
    - ``media_dir``: every file directly in this folder (images, ...)
      is one of this component's media assets.

    :meth:`gather_resources` collects this component's own resources
    (from the above folders) plus, recursively, every resource
    contributed by any :class:`Component` reachable through
    ``children`` — so a page composed of components can ask its
    top-level component for the *complete*, deduplicated set of assets
    it needs, without each component having to know about the ones
    nested inside it.

    A component that needs to place raw markup directly into the
    page's ``<head>`` — rather than a ``<link>``/``<script>`` tag
    generated from a resource file (an inline script that must run
    synchronously before first paint, for instance) — overrides
    :meth:`_own_head_markup`. :meth:`gather_head_markup` collects this
    the same recursive way as :meth:`gather_resources`.

    A component whose page-visible content lives in fields other than
    ``children`` (e.g. :class:`~builder.models.page.PageComponent`'s ``body``/
    ``head_extra``) overrides :meth:`_nested_components` to include
    those too.
    """

    css_dir: ClassVar[Path | None] = None
    js_dir: ClassVar[Path | None] = None
    media_dir: ClassVar[Path | None] = None

    resources: ResourceBundle | None = Field(
        default=None,
        description=(
            "Fixed, pre-built resources this component contributes, in "
            "addition to whatever css_dir/js_dir/media_dir glob up — for "
            "resources that don't fit the folder convention (a page's own "
            "page_dir assets, whose folder differs per instance; a "
            "generated file like a field manifest, which has no folder "
            "at all)."
        ),
    )

    def to_html(self) -> str:
        """Render this component's ``children`` (via
        :meth:`~builder.models.basic.html_tag.HtmlTag._inner_html`) — or
        ``""`` if it has none, e.g. a component that exists only to
        contribute ``resources``/head markup and has no markup of its
        own. A subclass whose HTML doesn't fit "just render my
        children" (e.g. one with its own wrapping tag, or page-visible
        content in fields other than ``children``) overrides this."""
        return self._inner_html()

    def _own_resources(self) -> ResourceBundle:
        """This component's own resources — from ``css_dir``/
        ``js_dir``/``media_dir`` plus the ``resources`` field — not
        including any child component's."""
        bundle = ResourceBundle(
            css=[Resource(source_path=path) for path in _list_files(self.css_dir, "*.css")],
            js=[Resource(source_path=path) for path in _list_files(self.js_dir, "*.js")],
            media=[Resource(source_path=path) for path in _list_files(self.media_dir, "*")],
        )
        if self.resources is not None:
            bundle = bundle.merge(self.resources)
        return bundle

    def _nested_components(self) -> list["Component"]:
        """Every direct child that is itself a :class:`Component`, to
        recurse into for resource-gathering. Default: scan ``children``.
        Override (extending, not replacing, this list) if page-visible
        content also lives in other fields."""
        return [child for child in self.children if isinstance(child, Component)]

    def gather_resources(self) -> ResourceBundle:
        """This component's own resources plus every nested component's,
        recursively — deduplicated by source file."""
        bundle = self._own_resources()
        for child in self._nested_components():
            bundle = bundle.merge(child.gather_resources())
        return bundle

    def _own_head_markup(self) -> list[str]:
        """Raw HTML this component needs placed directly into the
        page's ``<head>`` — not including any child component's.
        ``[]`` by default; override to contribute (e.g. an inline
        ``<script>`` that must run before first paint)."""
        return []

    def gather_head_markup(self) -> list[str]:
        """This component's own ``<head>`` markup plus every nested
        component's, recursively — in tree order, with exact-duplicate
        strings dropped."""
        markup = list(self._own_head_markup())
        for child in self._nested_components():
            markup += child.gather_head_markup()

        seen: set[str] = set()
        deduped = []
        for html in markup:
            if html in seen:
                continue
            seen.add(html)
            deduped.append(html)
        return deduped


def _list_files(directory: Path | None, pattern: str) -> list[Path]:
    if directory is None or not directory.is_dir():
        return []
    return sorted(path for path in directory.glob(pattern) if path.is_file())
