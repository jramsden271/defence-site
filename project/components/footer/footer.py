from builder.models.basic.p import P
from builder.models.basic.sectioning import Footer as FooterTag
from builder.models.component import Component


class Footer(Component):
    """The shared site ``<footer>``, for a
    :class:`~builder.models.page.PageComponent` to compose into its own
    output."""

    children: list = [
        FooterTag(
            custom_attributes={"class": "page-footer"},
            children=[P.from_text("&copy; 2026 [Company Name]. All rights reserved.")],
        )
    ]
