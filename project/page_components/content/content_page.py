from builder.models.component import Component
from builder.models.page import PageComponent
from project.page_components.shared.shared_assets import SharedAssets


class ContentPage(PageComponent):
    """
    A plain content page (see :class:`~builder.models.page.PageComponent`)
    — just a title and a ``body`` of arbitrary elements, no form or
    per-page assets of its own. Used for pages like the homepage that
    don't need anything a :class:`~project.page_components.defence_generator.defence_generator_page.DefenceGeneratorPage`
    provides.

    Adds :class:`~project.page_components.shared.shared_assets.SharedAssets`
    (the colour-variable/layout stylesheets, favicon, theme mechanism,
    and other plain shared scripts) to ``PageComponent``'s own
    ``Header``/``Footer`` — every other page-component that needs these
    includes ``SharedAssets`` the same explicit way.

    Usage from a page's ``build_page.py``::

        from project.page_components.content.content_page import ContentPage

        page = ContentPage(
            title="Defence generators",
            page_name="index",
            body=[...],
        )
        page.write(dist_dir, url="/")
    """

    def _nested_components(self) -> list[Component]:
        return [*super()._nested_components(), SharedAssets()]
