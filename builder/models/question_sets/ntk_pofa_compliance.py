"""
The reusable Notice to Keeper (NtK) / PoFA-compliance question set.

Whether a keeper-defendant received an NtK, and if so, whether it meets the
content and timing requirements of PoFA 2012 Schedule 4 paragraph 9 to
transfer liability from driver to keeper, is relevant to *every*
defence-generator page where that transfer might be in issue — not just one
specific defence. This bundles that fixed set of questions (and their field
names/wiring) so a page doesn't have to redefine them.

Field names are fixed (``receivedNtk``, ``ntkDate``, ``ntkHasParkingPeriod``,
...) rather than page-assignable:
``page_templates/defence_generator/js/pofa_date.js`` and each page's
``generate_defence.js`` read ``formValues.ntkDate`` by that exact name, so
every page using this set shares the same JS-facing contract.

This deliberately covers the more commonly-seen ways NtKs fail to comply
— not an exhaustive list of every Schedule 4 paragraph 9 requirement.

Legal accuracy note: the content-requirement questions beyond timing and
parking period (keeper-liability warning, sum payable, terms-and-conditions
reference) are drafted from a general understanding of Schedule 4 paragraph
9 and have not been checked against the exact statutory wording — review
before relying on them (see the ``NOTE(legal-review)`` comment below).

Usage from a page's ``build_page.py``::

    from builder.models.question_sets.ntk_pofa_compliance import (
        NtkPofaComplianceQuestions,
    )

    ntk = NtkPofaComplianceQuestions()
    # Optional: extend/override any question's help for this page.
    ntk.ntk_has_parking_period.question.set_help(HELP["parking_period_no_stopping"])

    form = Form(
        id="profileForm",
        elements=[
            ...,
            *ntk.elements(),
            ...,
        ],
    )

Each control is also exposed directly as an attribute (e.g.
``ntk.received_ntk``, ``ntk.ntk_date``), so a page can build ``.when(...)``
dependencies off them or drop them into a custom layout instead of calling
:meth:`elements`.
"""

from builder.models.basic.base_element import BaseElement
from builder.models.div.form_group import FormGroup
from builder.models.div.form_group_2 import FormGroup2
from builder.models.forms.date_input import DateInput
from builder.models.forms.radio.radio_group import RadioGroup
from builder.models.questions.multiple_choice_question import MultipleChoiceQuestion
from builder.models.questions.single_question import SingleQuestion


class NtkPofaComplianceQuestions:
    """The standard NtK/PoFA-compliance question block: did the keeper
    receive an NtK, and if so, its issue date plus the most commonly-seen
    content defects (missing parking period, missing keeper-liability
    warning, missing sum-payable/discount terms, missing terms-and-
    conditions reference). Each question can be further customised (e.g.
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
        ntk_has_parking_period_q.add_option("Not sure","notsure")
        ntk_has_parking_period_q.options[0].description = "May include \"parking period\", \"period of parking\", \"start and end time\", or \"duration of parking\""
        ntk_has_parking_period_q.set_help("PoFA was seemingly written to handle parking overstays, yet is often deployed by parking operators for other misdemeanours, such as parking out of hours, stopping in a no-stopping zone, or parking out of bay. For these more exotic cases, PoFA does not provide much guidance on what constitutes a parking period, so this is a bit of a grey zone.\n\nIf the NtK shows some kind of a start and an end time, or a parking duration, then this is likely valid, so choose 'yes'.\n\nIf the NtK shows a single time, or a single time with the phrase like 'the period immediately preceding [time]', then this can be contested, so choose 'no'.\n\nIf it is not even alleged that you parked, (e.g. if the allegation concerns a no-stopping zone) then this is likely a 'no'.\n\nIf you choose 'no', you may need to manually edit the defence to tailor it to your situation and the NtK's exact wording regarding times.\n\nSelect 'not sure' to skip this one.")
        self.ntk_has_parking_period = RadioGroup(
            name="ntkHasParkingPeriod", question=ntk_has_parking_period_q
        )

        ntk_complies_with_para_9_4_q = MultipleChoiceQuestion(
            display_question="Does the NtK comply with PoFA Sch.4 paragraph 9(4) regarding keeper liability when the driver details are not known?"
        )
        ntk_complies_with_para_9_4_q.add_yes_no_options()
        ntk_complies_with_para_9_4_q.set_help("""<p>For liability to transfer from driver to keeper, the NtK must invite the keeper to either pay the charge or identify the driver, and warn that if neither happens, the keeper will be held liable for the charge as if they were the driver.</p><p>There is some very exact wording within PoFA Sch.4 para 9 (4). The NtK should contain the following text, either word for word exact, or <em>very</em> close to it:</p><div class=\"summary-subbox\"><p>
        warn the keeper that if, after the period of 28 days beginning with the day after that on which the notice is given—</p><p>

        \t(i)the amount of the unpaid parking charges specified under paragraph (d) has not been paid in full, and</p><p>

        \t(ii)the creditor does not know both the name of the driver and a current address for service for the driver,</p><p>

        the creditor will (if all the applicable conditions under this Schedule are met) have the right to recover from the keeper so much of that amount as remains unpaid</p></div>
                                               """)
        self.ntk_complies_with_para_9_4 = RadioGroup(question=ntk_complies_with_para_9_4_q)

        ntk_states_land_q = MultipleChoiceQuestion(
            display_question="Does the NtK specify the land on which it was parked?"
        )
        ntk_states_land_q.add_option("Yes")
        ntk_states_land_q.add_option("Yes - vaguely","vaguely","e.g. 'Birmingham City Centre' as a parking location is too vague. The location should generally identify a particular car park or street.")
        ntk_states_land_q.add_option("Yes - but it's wrong","wrong","Check the location in the NtK carefully. Sometimes a neighbouring car park will be given instead of the correct location.")
        ntk_states_land_q.add_option("No","no","No location is specified at all.")

        self.ntk_states_land = RadioGroup(question=ntk_states_land_q)


    def elements(self) -> list[str | BaseElement]:
        """The standard form-fragment layout for this question set: the
        received_ntk question, then a conditional follow-up block (shown
        only when the answer is "yes") with the NtK date and content-
        requirement questions. Ready to splice into a page's
        ``Form.elements``."""
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
                    self.ntk_complies_with_para_9_4,
                    self.ntk_states_land,
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
