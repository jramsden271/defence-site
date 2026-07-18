"""
Build test.html from Python element classes.

Run from the ``builder`` directory:

    python run_builder.py

This produces ``test.html`` (one level up) that is functionally equivalent to
``run.html``. Focus here on the *questions and answers* — questions (their
label, help text and possible answers) are plain data; the control classes
(``RadioGroup``, ``DateInput``, ...) render that data as HTML, and
dependencies between questions are expressed with ``some_control.when("value")``.
"""

from pathlib import Path

from field_manifest import write_manifest
from help_text import load_help_text
from models.basic.base_element import assign_names_from_globals
from models.basic.div import Div
from models.div.form_group import FormGroup
from models.div.form_group_2 import FormGroup2
from models.forms.button import Button
from models.forms.date_input import DateInput
from models.forms.form import Form
from models.forms.radio.radio_group import RadioGroup
from models.questions.multiple_choice_question import MultipleChoiceQuestion
from models.questions.question_option import QuestionOption
from models.questions.single_question import SingleQuestion

script_dir = Path(__file__).parent
page_dir = script_dir.parent / "pages" / "no_stopping_defence"

# Help text is page content, not code — loaded from the page's own
# help_text.json rather than hardcoded here. Look up entries by key and pass
# to a question's set_help(), e.g. pronouns_q.set_help(HELP["pronouns_why"]).
HELP = load_help_text(page_dir / "help_text.json")


# ---------------------------------------------------------------------------
# Questions
# ---------------------------------------------------------------------------

pronouns_q = MultipleChoiceQuestion(display_question="What are your pronouns?")
pronouns_q.add_option(label="They/Them", value="neutral")
pronouns_q.add_option(label="He/Him", value="male")
pronouns_q.add_option(label="She/Her", value="female")
pronouns_q.set_help(HELP["pronouns_why"])
pronouns = RadioGroup(question=pronouns_q)

defend_as_q = MultipleChoiceQuestion(display_question="Are you defending as the Registered Keeper only, or as the Driver too?")
defend_as_q.add_option(
    "Registered Keeper only",
    value="keeper",
    description="Select if you are the registered keeper and have not previously admitted to being the driver (whether or not you were the driver, or you can't recall). Defendants are often in a stronger legal position if they don't admit to being the driver.",
)
defend_as_q.add_option(
    "Registered Keeper and driver",
    value="driver",
    description="Select if you have previously admitted to being the driver, or you were the driver AND you have a strong reason for making this a part of your case (e.g. you have mitigating circumstances that require you to reveal that you were the driver).",
)
defend_as = RadioGroup(question=defend_as_q)

incident_land_q = MultipleChoiceQuestion(
    display_question="What land did the incident take place on?",
    options=[
        QuestionOption(label="Railway land", value="railway"),
        QuestionOption(label="Other land under statutory control",value="airport", description="This includes land under the control of a local authority, airport, or other statutory body. It is usually land where byelaws are in place."),
        QuestionOption(label="Other private land / Not sure", value="other"),
    ],
)
incident_land_q.set_help(HELP["relevant_land"])
incident_land = RadioGroup(question=incident_land_q)

has_incident_date = RadioGroup(
    question=MultipleChoiceQuestion(
        display_question="Do the Particulars of Claim show the date of when the incident(s) occurred?",
        options=[
            QuestionOption(label="Yes - a single date", value="single"),
            QuestionOption(label="Yes - a range of dates", value="range"),
            QuestionOption(label="No", value="no"),
        ],
    ),
)

received_ntk_q = MultipleChoiceQuestion(display_question="Did you receive a Notice to Keeper (NtK)?")
received_ntk_q.add_yes_no_options()
received_ntk = RadioGroup(question=received_ntk_q)

ntk_has_parking_period_q = MultipleChoiceQuestion(display_question="Does the NtK show a parking period?")
ntk_has_parking_period_q.add_yes_no_options()
ntk_has_parking_period_q.set_help(HELP["parking_period"])
ntk_has_parking_period = RadioGroup(question=ntk_has_parking_period_q)

incident_date = DateInput(question=SingleQuestion(display_question="Date of the incident:"))
ntk_date = DateInput(question=SingleQuestion(display_question="Issue date of the Notice to Keeper (NtK):"))


# Backfill each control's `name` (used as the HTML name/id and data-trigger
# key) from the variable it's assigned to, so questions above don't have to
# repeat name="..." matching the variable name.
assign_names_from_globals(globals())


# ---------------------------------------------------------------------------
# Form assembly
# ---------------------------------------------------------------------------

form = Form(
    id="profileForm",
    elements=[
        # Standalone questions
        FormGroup(elements=[pronouns]),
        FormGroup(elements=[defend_as]),
        FormGroup2(
            show_when=defend_as.when("keeper"),
            elements=[incident_land],
        ),
        # Incident date
        FormGroup(elements=[has_incident_date]),
        FormGroup2(
            show_when=has_incident_date.when("single"),
            elements=[incident_date],
        ),
        FormGroup2(
            show_when=has_incident_date.when("range"),
            elements=[HELP["date_range_explanation"].body],
        ),
        FormGroup2(
            show_when=has_incident_date.when("no"),
            elements=["If no date is specified at all, consider using the Chan and Akande defence."],
        ),
        # Notice to Keeper (keeper only)
        Div(
            show_when=defend_as.when("keeper"),
            elements=[
                FormGroup(elements=[received_ntk]),
                FormGroup2(
                    show_when=received_ntk.when("yes"),
                    elements=[
                        "The NtK must meet some strict requirements to allow "
                        "liability to be transferred from the driver to the "
                        "keeper. These questions will help establish whether it "
                        "meets those requirements.",
                        ntk_date,
                        ntk_has_parking_period,
                    ],
                ),
                FormGroup2(
                    show_when=received_ntk.when("no"),
                    elements=[
                        "This form is currently set up for defendants who have "
                        "received a Notice to Keeper (NtK). This form is currently "
                        "not set up for Notice to Hirer (NtH)."
                    ],
                ),
            ],
        ),
        # Submit
        Button(text="Generate Defence", onclick="generateText()", extra_css_classes=["btn-center"]),
    ],
)


# ---------------------------------------------------------------------------
# Render page
# ---------------------------------------------------------------------------

layout_dir = page_dir / "layout"

html = ""
with open(layout_dir / "blocks" / "header.html", "r", encoding="utf-8") as f:
    html += f.read()

html += "\n" + form.to_html() + "\n"

with open(layout_dir / "blocks" / "footer.html", "r", encoding="utf-8") as f:
    html += f.read()

with open(script_dir.parent / "test.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Wrote {script_dir.parent / 'test.html'}")

manifest_path = script_dir.parent / "js" / "form_variables.js"
write_manifest(form, manifest_path)
print(f"Wrote {manifest_path}")
