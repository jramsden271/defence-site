"""
Build test.html from Python element classes.

Run from the ``builder`` directory:

    python run_builder.py

This produces ``test.html`` (one level up) that is functionally equivalent to
``run.html``. Focus here on the *questions and answers* — the element classes
handle the HTML, and dependencies between questions are expressed with
``some_group.when("value")``.
"""

from pathlib import Path

from field_manifest import write_manifest
from helpers import question
from models.basic.base_element import assign_names_from_globals
from models.div.form_group import FormGroup
from models.div.form_group_2 import FormGroup2
from models.div.form_group_container import FormGroupContainer
from models.forms.button import Button
from models.forms.date_input import DateInput
from models.widgets.expanding_textbox import ExpandingTextbox
from models.forms.form import Form
from models.forms.radio.radio_group import RadioGroup
from models.forms.radio.radio_item import RadioItem


# ---------------------------------------------------------------------------
# Questions
# ---------------------------------------------------------------------------

pronouns = RadioGroup(label="What are your pronouns?")
pronouns.add_option(label="They/Them", value="neutral")
pronouns.add_option(label="He/Him", value="male")
pronouns.add_option(label="She/Her", value="female")
pronouns.add_help("Why are you asking this?",'This is only used to ensure that the generated text uses the correct pronouns when referring to you. If you prefer not to specify, select "They/Them".')

defend_as = RadioGroup(label="Are you defending as the Registered Keeper only, or as the Driver too?")
defend_as.add_option(
    "Registered Keeper only",
    value="keeper",
    description="Select if you are the registered keeper and have not previously admitted to being the driver (whether or not you were the driver, or you can't recall). Defendants are often in a stronger legal position if they don't admit to being the driver.",
)
defend_as.add_option(
    "Registered Keeper and driver",
    value="driver",
    description="Select if you have previously admitted to being the driver, or you were the driver AND you have a strong reason for making this a part of your case (e.g. you have mitigating circumstances that require you to reveal that you were the driver).",
)

incident_land = RadioGroup(
    label="What land did the incident take place on?",
    items=[
        RadioItem(label="Railway land", value="railway"),
        RadioItem(label="Other land under statutory control",value="airport", description="This includes land under the control of a local authority, airport, or other statutory body. It is usually land where byelaws are in place."),
        RadioItem(label="Other private land / Not sure", value="other"),
    ],
    help=[
        "This is important because certain types of land are not considered "
        "'relevant land' under the Protection of Freedoms Act 2012, in which "
        "case, it is generally not possible to transfer liability to the "
        "keeper. If the incident happened on non-relevant land, the "
        "defendant is at a great advantage!",
        "Airport land and railway land generally include access roads, car "
        "parks and facilities immediately serving those lands. The boundary "
        "is dictated by where byelaws are in place. The boundary can be "
        "surprisingly large, and at some airports includes nearby hotels and "
        "fast food restaurant car parks. If you are not sure whether the "
        "incident happened on relevant land, it can be helpful to find a map "
        "with the boundary where byelaws are in place, or ask a question in "
        "the relevant forum.",
    ],
)

has_incident_date = RadioGroup(
    label="Do the Particulars of Claim show the date of when the incident(s) occurred?",
    items=[
        RadioItem(label="Yes - a single date", value="single"),
        RadioItem(label="Yes - a range of dates", value="range"),
        RadioItem(label="No", value="no"),
    ],
)

received_ntk = RadioGroup(label="Did you receive a Notice to Keeper (NtK)?")
received_ntk.add_yes_no_options()

ntk_has_parking_period = RadioGroup(label="Does the NtK show a parking period?")
ntk_has_parking_period.add_yes_no_options()
ntk_has_parking_period.add_help("What is a parking period?", "A valid NtK must show a parking period, which is the time during which the vehicle was parked and the alleged incident occurred. This is usually shown as a start and end time, or a total duration of parking. For no-stopping cases, it is unlikely that the NtK meets this requirement.")


# Backfill each group's `name` (used as the HTML name/id and data-trigger key)
# from the variable it's assigned to, so questions above don't have to repeat
# name="..." matching the variable name.
assign_names_from_globals(globals())


# ---------------------------------------------------------------------------
# Form assembly
# ---------------------------------------------------------------------------

form = Form(
    id="profileForm",
    elements=[
        # Standalone questions
        question(pronouns),
        question(defend_as),
        question(incident_land, show_when=defend_as.when("keeper")),
        # Incident date
        FormGroupContainer(
            elements=[
                FormGroup(elements=[has_incident_date]),
                FormGroup2(
                    show_when=has_incident_date.when("single"),
                    elements=[DateInput(id="incidentDate", label="Date of the incident:")],
                ),
                FormGroup2(
                    show_when=has_incident_date.when("range"),
                    elements=[
                        "A date range normally means that the Claimant has "
                        "alleged multiple incidents within a specific time frame. "
                        "This requires a slightly different approach, which this "
                        "tool currently does not support. You can try selecting a "
                        "single date and proceeding from there, or if the date "
                        "range is vague enough, it may make more sense to use the "
                        "Chan and Akande defence."
                    ],
                ),
                FormGroup2(
                    show_when=has_incident_date.when("no"),
                    elements=[
                        "If no date is specified at all, consider using the Chan "
                        "and Akande defence."
                    ],
                ),
            ],
        ),
        # Notice to Keeper (keeper only)
        FormGroupContainer(
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
                        DateInput(
                            id="ntkDate",
                            label="Issue date of the Notice to Keeper (NtK):",
                        ),
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
        Button(text="Generate Defence", onclick="generateText()"),
    ],
)


# ---------------------------------------------------------------------------
# Render page
# ---------------------------------------------------------------------------

script_dir = Path(__file__).parent

html = ""
with open(script_dir / "layout" / "blocks" / "header.html", "r", encoding="utf-8") as f:
    html += f.read()

html += "\n" + form.to_html() + "\n"

with open(script_dir / "layout" / "blocks" / "footer.html", "r", encoding="utf-8") as f:
    html += f.read()

with open(script_dir.parent / "test.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Wrote {script_dir.parent / 'test.html'}")

manifest_path = script_dir.parent / "js" / "form_variables.js"
write_manifest(form, manifest_path)
print(f"Wrote {manifest_path}")
