from builder.models.basic.heading import H2
from builder.models.basic.html_tag import HtmlTag
from builder.models.basic.p import P
from builder.models.component import Component


class Intro(Component):
    """The introductory copy for the no-stopping defence generator page,
    placed above its form. Has no wrapping tag of its own — its
    ``children`` (an ``<h2>`` followed by three ``<p>``s) render
    directly as page content, same as the ``.html`` fragment this
    replaced."""

    children: list["str | HtmlTag"] = [
        H2(children=["No stopping defence generator"]),
        P.from_text(
            "This tool is designed to help you generate a defence to a "
            "MCOL claim, where the claimant alleges that you contravened "
            "a 'no stopping' rule on private land. It is intended for use "
            "in England and Wales, where the Protection of Freedoms Act "
            "2012 (PoFA) applies. In Scotland and Northern Ireland, "
            "things are <em>different</em>."
        ),
        P.from_text(
            "The output of this tool is unlikely to exactly match your "
            "circumstances, but it should provide a useful starting point "
            "for your defence. Review the output carefully, and feel free "
            "to edit as needed."
        ),
        P.from_text(
            "Note: The generated text is for informational purposes only "
            "and should not be considered legal advice. Always consult "
            "with a qualified legal professional for advice specific to "
            "your situation."
        ),
    ]
