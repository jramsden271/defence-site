"""
Build dist/ntk_compliance_check.html from Python element classes.

Run via the repo-root entry point:

    python builder/build_everything.py

This is a ``defence_generator`` page (see
``page_templates/defence_generator/render_defence_generator.py``), same as
``pages/no_stopping_defence``. Unlike that page, this one assumes the
reader already has an NtK in hand and wants to check it for compliance —
so it asks the incident date, then the standard
:class:`~builder.models.question_sets.ntk_pofa_compliance.NtkPofaComplianceQuestions`
questions unconditionally (via ``FormGroup``, not ``FormGroup2`` — there's
no "did you receive an NtK?" gate here, since receiving one is assumed),
and generates paragraphs explaining any compliance defects found.
"""

from pathlib import Path

from builder.models.basic.base_element import assign_names_from_globals
from builder.models.div.form_group import FormGroup
from builder.models.forms.button import Button
from builder.models.forms.date_input import DateInput
from builder.models.forms.form import Form
from builder.models.question_sets.ntk_pofa_compliance import NtkPofaComplianceQuestions
from builder.models.questions.single_question import SingleQuestion
from page_templates.defence_generator.render_defence_generator import (
    render_defence_generator,
)

page_dir = Path(__file__).parent
repo_root = page_dir.parent.parent
dist_dir = repo_root / "dist"


# ---------------------------------------------------------------------------
# Questions
# ---------------------------------------------------------------------------

incident_date = DateInput(question=SingleQuestion(display_question="Date of the incident:"))

# The standard NtK/PoFA-compliance question block. This page assumes the
# reader already has an NtK, so it asks the compliance questions directly —
# no received_ntk gate.
ntk = NtkPofaComplianceQuestions()


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
        FormGroup(elements=[incident_date]),
        *[FormGroup(elements=[element]) for element in ntk.elements()],
        # Submit
        Button(text="Check Compliance", onclick="generateDefence()", extra_css_classes=["btn-center"]),
    ],
)


# ---------------------------------------------------------------------------
# Render page
# ---------------------------------------------------------------------------

intro_html = (page_dir / "blocks" / "intro.html").read_text(encoding="utf-8")

html = render_defence_generator(
    title="Is your NtK valid?",
    page_name="ntk_compliance_check",
    intro_html=intro_html,
    form=form,
    dist_dir=dist_dir,
    page_dir=page_dir,
)

dist_dir.mkdir(parents=True, exist_ok=True)

output_path = dist_dir / "ntk_compliance_check.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Wrote {output_path}")
