from builder.models.basic.div import Div
from builder.models.basic.em import Em
from builder.models.basic.heading import H3
from builder.models.component import Component
from builder.models.forms.button import Button


class OutputBox(Component):
    """The output area shared by every defence-generator page: the PoFA
    result line, the generated defence paragraphs, a running character
    count, and a copy-to-clipboard button. ``children`` replaces the
    ``output_box.html`` fragment this used to be read from."""

    children: list = [
        Div(
            id="output-box",
            children=[
                H3(children=["PoFA results:"]),
                Div(id="pofaResultsContainer"),
                H3(children=["Defence:"]),
                Em.from_text("Review this defence carefully before submitting it to the court."),
                Div(id="paragraphsContainer"),
                Div(
                    id="charCount",
                    custom_attributes={
                        "style": (
                            "font-size: 14px; color: var(--color-text-muted); "
                            "margin-bottom: 10px; font-weight: bold;"
                        ),
                    },
                    children=["Character Count: 0"],
                ),
                Button(
                    children=["Copy Text"],
                    id="copyBtn",
                    onclick="copyToClipboard()",
                    custom_attributes={"class": "btn btn-secondary"},
                ),
            ],
        )
    ]
