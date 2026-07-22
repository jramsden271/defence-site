from builder.models.basic.heading import H2
from builder.models.basic.html_tag import HtmlTag
from builder.models.basic.p import P
from builder.models.component import Component


class Intro(Component):
    """The introductory copy for the NtK compliance-check page, placed
    above its form. Has no wrapping tag of its own — its ``children``
    (an ``<h2>`` followed by three ``<p>``s) render directly as page
    content, same as the ``.html`` fragment this replaced."""

    children: list["str | HtmlTag"] = [
        H2(children=["Is your NtK valid?"]),
        P.from_text(
            "This tool checks a Notice to Keeper (NtK) you've already "
            "received against the requirements of the Protection of "
            "Freedoms Act 2012 (PoFA) Schedule 4. It is intended for use "
            "in England and Wales, where PoFA applies. In Scotland and "
            "Northern Ireland, things are <em>different</em>."
        ),
        P.from_text(
            "Answer the questions below based on what your NtK actually "
            "says. The tool will explain any defects found — these can "
            "form the basis of a defence if the parking operator later "
            "brings a claim."
        ),
        P.from_text(
            "Note: The generated text is for informational purposes only "
            "and should not be considered legal advice. Always consult "
            "with a qualified legal professional for advice specific to "
            "your situation."
        ),
    ]
