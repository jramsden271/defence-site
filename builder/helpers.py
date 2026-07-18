"""
Small convenience builders for assembling the form with less boilerplate.

These are thin wrappers over the element classes — they only exist to remove
repetition from ``run_builder.py``.
"""

from models.basic.base_element import Dependency, Triggerable
from models.div.form_group import FormGroup
from models.div.form_group_2 import FormGroup2
from models.div.form_group_container import FormGroupContainer


def question(
    control: Triggerable, show_when: Dependency | None = None
) -> FormGroupContainer:
    """
    Wrap a standalone question control (e.g. a ``RadioGroup`` or ``DateInput``)
    in the usual ``form-group-container`` > ``form-group`` layout.

    ``show_when`` (e.g. ``defend_as.when("keeper")``) makes the question
    conditional; it is applied to the inner ``form-group`` so the control shows
    or hides as a unit.
    """
    if show_when == None:
        return FormGroupContainer(
            elements=[FormGroup(show_when=show_when, elements=[control])]
        )
    else:
        return FormGroupContainer(
            elements=[FormGroup2(show_when=show_when, elements=[control])]
        )
