"""
The reusable Notice to Keeper (NtK) / PoFA-compliance question set.

Whether a keeper-defendant received an NtK, and if so, whether it was
issued in time and shows a parking period, is relevant to *every*
defence-generator page where liability might transfer from driver to
keeper under PoFA 2012 — not just one specific defence. This bundles that
fixed set of questions (and their field names/wiring) so a page doesn't
have to redefine them.

Field names are fixed (``receivedNtk``, ``ntkDate``, ``ntkHasParkingPeriod``)
rather than page-assignable: ``page_templates/defence_generator/js/pofa_date.js``
and ``generate_defence.js`` read ``formValues.ntkDate`` by that exact name,
so every page using this set shares the same JS-facing contract.

Usage from a page's ``build_page.py``::

    from builder.models.question_sets.ntk_pofa_compliance import (
        NtkPofaComplianceQuestions,
    )

    ntk = NtkPofaComplianceQuestions()
    # Optional: extend/override any question's help for this page.
    ntk.ntk_has_parking_period_q.set_help(HELP["parking_period_no_stopping"])

    form = Form(
        id="profileForm",
        elements=[
            ...,
            *ntk.elements(),
            ...,
        ],
    )

Each control (``received_ntk``, ``ntk_date``, ``ntk_has_parking_period``) is
also exposed directly, so a page can build ``.when(...)`` dependencies off
them or drop them into a custom layout instead of calling :meth:`elements`.
"""

from builder.models.basic.div import Div
from builder.models.div.form_group import FormGroup
from builder.models.div.form_group_2 import FormGroup2
from builder.models.basic.base_element import BaseElement
from builder.models.forms.date_input import DateInput
from builder.models.forms.radio.radio_group import RadioGroup
from builder.models.questions.base_question import HelpText
from builder.models.questions.multiple_choice_question import MultipleChoiceQuestion
from builder.models.questions.single_question import SingleQuestion

_PARKING_PERIOD_HELP = HelpText(
    title="What is a parking period?",
    body=(
        "A valid NtK must show a parking period, which is the time during "
        "which the vehicle was parked and the alleged incident occurred. "
        "This is usually shown as a start and end time, or a total "
        "duration of parking."
    ),
)


class NtkPofaComplianceQuestions:
    """The standard NtK/PoFA-compliance question block: did the keeper
    receive an NtK, and if so, its issue date and whether it shows a
    parking period. Each question can be further customised (e.g.
    ``.set_help(...)``) before the page builds its ``Form``.
    """

    def __init__(self) -> None:
        received_ntk_q = MultipleChoiceQuestion(
            display_question="Did you receive a Notice to Keeper (NtK)?"
        )
        received_ntk_q.add_yes_no_options()
        self.received_ntk = RadioGroup(name="receivedNtk", question=received_ntk_q)

        self.ntk_date = DateInput(
            name="ntkDate",
            question=SingleQuestion(
                display_question="Issue date of the Notice to Keeper (NtK):"
            ),
        )

        ntk_has_parking_period_q = MultipleChoiceQuestion(
            display_question="Does the NtK show a parking period?"
        )
        ntk_has_parking_period_q.add_yes_no_options()
        ntk_has_parking_period_q.set_help(_PARKING_PERIOD_HELP)
        self.ntk_has_parking_period = RadioGroup(
            name="ntkHasParkingPeriod", question=ntk_has_parking_period_q
        )

    def elements(self) -> list[str | BaseElement]:
        """The standard form-fragment layout for this question set: the
        received_ntk question, then a conditional follow-up block (shown
        only when the answer is "yes") with the NtK date and parking-period
        questions. Ready to splice into a page's ``Form.elements``."""
        return [
            FormGroup(elements=[self.received_ntk]),
            FormGroup2(
                show_when=self.received_ntk.when("yes"),
                elements=[
                    "The NtK must meet some strict requirements to allow "
                    "liability to be transferred from the driver to the "
                    "keeper. These questions will help establish whether it "
                    "meets those requirements.",
                    self.ntk_date,
                    self.ntk_has_parking_period,
                ],
            ),
            FormGroup2(
                show_when=self.received_ntk.when("no"),
                elements=[
                    "This form is currently set up for defendants who have "
                    "received a Notice to Keeper (NtK). This form is "
                    "currently not set up for Notice to Hirer (NtH)."
                ],
            ),
        ]
