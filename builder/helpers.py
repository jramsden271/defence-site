"""
Small convenience builders for assembling the form with less boilerplate.

These are thin wrappers over the element classes — they only exist to remove
repetition from ``run_builder.py``.
"""

from models.basic.base_element import Dependency
from models.div.form_group import FormGroup
from models.div.form_group_2 import FormGroup2
from models.div.form_group_container import FormGroupContainer
from models.forms.radio.radio_group import RadioGroup


def question(
    group: RadioGroup, show_when: Dependency | None = None
) -> FormGroupContainer:
    """
    Wrap a standalone question in the usual ``form-group-container`` >
    ``form-group`` layout.

    ``show_when`` (e.g. ``defend_as.when("keeper")``) makes the question
    conditional; it is applied to the inner ``form-group`` so the control shows
    or hides as a unit.
    """
    if show_when == None:
        return FormGroupContainer(
            elements=[FormGroup(show_when=show_when, elements=[group])]
        )
    else:
        return FormGroupContainer(
            elements=[FormGroup2(show_when=show_when, elements=[group])]
        )
