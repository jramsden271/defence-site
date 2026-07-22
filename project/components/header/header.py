from builder.models.basic.a import A
from builder.models.basic.nav import Nav
from builder.models.basic.sectioning import Header as HeaderTag
from builder.models.component import Component
from builder.models.forms.button import Button


class Header(Component):
    """The shared site ``<header>``, for a
    :class:`~builder.models.page.PageComponent` to compose into its own
    output."""

    children: list = [
        HeaderTag(
            custom_attributes={"class": "page-header"},
            children=[
                A.from_text(
                    "🚗",
                    href="index.html",
                    custom_attributes={"class": "site-logo", "aria-label": "Home"},
                ),
                Nav(
                    custom_attributes={"class": "page-header-nav"},
                    children=[
                        A.from_text("No stopping defence generator", href="no-stopping-defence.html"),
                        A.from_text("Is your NtK valid?", href="ntk-compliance-check.html"),
                        Button(
                            id="themeToggle",
                            custom_attributes={"class": "theme-toggle", "aria-label": "Toggle dark mode"},
                        ),
                    ],
                ),
            ],
        )
    ]
