from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from builder.models.questions.base_question import HelpText


class Dependency(BaseModel):
    """
    Describes a visibility condition: the element carrying this dependency is
    only shown when the referenced trigger currently holds ``value``.

    Instances are normally created via :meth:`Triggerable.when`, so that the
    trigger id is derived from the source element rather than typed by hand.
    """

    trigger: str
    value: str

    def attrs(self) -> str:
        """Return the ``data-depends-on``/``data-value`` attribute string
        (including the leading space) used to make an element conditional."""
        return f' data-depends-on="{self.trigger}" data-value="{self.value}"'


def normalise_children(value):
    """Coerce a container's ``elements`` input into a list of elements.

    Accepts a single item or a list, and wraps any plain string in a
    :class:`~models.basic.p.P` paragraph so text blocks can be written as
    ``elements=["some text"]``. Used as a ``mode="before"`` field validator.
    """
    # Imported lazily to avoid a circular import (P subclasses Conditional).
    from builder.models.basic.p import P

    if isinstance(value, (str, BaseElement)):
        value = [value]
    return [P(text=item) if isinstance(item, str) else item for item in value]


class BaseElement(BaseModel):
    """
    Base class for all elements in the model.

    It deliberately has no visibility or trigger behaviour of its own — those
    are opt-in via the :class:`Conditional` and :class:`Triggerable` mixins, so
    an element only carries the fields it can actually use.

    ``extra="forbid"`` means passing a field an element doesn't support (e.g.
    ``depends_on`` to a non-:class:`Conditional` element) raises instead of
    being silently ignored.
    """

    model_config = ConfigDict(extra="forbid")

    # A fixed, structural CSS class string for this kind of element (e.g.
    # "radio-group govuk-radio-group" for RadioGroup, "form-group-2" for
    # FormGroup2). It's a ClassVar, not a pydantic field, so it's a true
    # class-level constant: it can't be passed to __init__, set per-instance,
    # or appear in model_dump()/schema — only overridden by subclassing.
    # Elements with no single top-level tag can leave this at "".
    base_css_classes: ClassVar[str] = ""

    # Additional CSS classes to append alongside base_css_classes. Additive
    # rather than a replacement, so the structural class above can never be
    # accidentally dropped by a caller reaching for extra styling.
    extra_css_classes: list[str] = []

    def _css_classes(self) -> str:
        """This element's ``base_css_classes`` plus any ``extra_css_classes``
        (space-joined). Elements with no single top-level tag can simply not
        call this — ``extra_css_classes`` then goes unused, which is safe.
        """
        if not self.extra_css_classes:
            return self.base_css_classes
        return " ".join([self.base_css_classes, *self.extra_css_classes])

    def to_html(self) -> str:
        """
        Convert the element to its HTML representation.
        """
        raise NotImplementedError("Subclasses must implement this method.")


class Conditional(BaseElement):
    """
    Mixin for elements that can be conditionally shown/hidden.

    Set ``depends_on`` (usually via a trigger's ``.when(value)``) to render the
    element hidden until the front-end script reveals it. This is a property of
    *layout* elements (e.g. :class:`~models.basic.div.Div`), not of controls.
    """

    # When set, the element is rendered hidden and only revealed by the
    # front-end script when the dependency is satisfied.
    show_when: Dependency | None = None

    def _visibility_attrs(self) -> str:
        """Attributes + inline style that make an element conditionally shown.

        Returns an empty string for unconditional elements.
        """
        if self.show_when is None:
            return ""
        return f'{self.show_when.attrs()} style="display:none;"'


class Triggerable(BaseElement):
    """
    Mixin for elements whose current answer can control the visibility of
    other elements (e.g. radio groups).

    The element exposes a ``data-trigger`` id of ``"{name}Trigger"`` and lets
    dependents reference a specific answer via :meth:`when`. It is *not* itself
    conditional — to hide a control, wrap it in a :class:`Conditional` element
    (typically a :class:`~models.basic.div.Div`).

    ``name`` may be left unset at construction time and backfilled later (e.g.
    via :func:`assign_names_from_globals`) from the variable it's assigned to,
    so a module doesn't have to repeat ``pronouns = RadioGroup(name="pronouns", ...)``.
    """

    name: str = ""

    @property
    def trigger_id(self) -> str:
        return f"{self.name}Trigger"

    def when(self, value: str) -> Dependency:
        """Return a :class:`Dependency` satisfied when this control's answer
        equals ``value``. Use it for a dependent element's ``depends_on``."""
        return Dependency(trigger=self.trigger_id, value=value)


def _to_camel_case(snake_case: str) -> str:
    """Convert a ``snake_case`` identifier to ``camelCase``."""
    first, *rest = snake_case.split("_")
    return first + "".join(word.title() for word in rest)


def assign_names_from_globals(namespace: dict) -> None:
    """Backfill unset ``Triggerable.name`` fields from their variable name.

    Call this once, at the bottom of a builder module, with ``globals()``.
    Any module-level variable bound to a :class:`Triggerable` that was
    constructed without ``name=`` gets ``name`` set to the camelCase form of
    the variable it's assigned to (e.g. ``has_incident_date`` -> ``hasIncidentDate``),
    matching the ``name``/``data-trigger`` convention used elsewhere (HTML
    attributes, JS), so questions can be written as
    ``pronouns = RadioGroup(label="...")`` instead of repeating the name.
    """
    for var_name, value in namespace.items():
        if isinstance(value, Triggerable) and not value.name:
            value.name = _to_camel_case(var_name)


def render_help(help: "HelpText | None") -> str:
    """Render a question's help text as an ``ExpandingTextbox`` block (prefixed
    with a newline), or "" if ``help`` is unset or has an empty body.

    Controls call this with ``self.question.help`` — building an
    ``ExpandingTextbox`` is an HTML concern, so it lives here rather than on
    the question classes (see
    :class:`~models.questions.base_question.BaseQuestion`). A ``None`` title
    falls back to ``ExpandingTextbox``'s own default title.
    """
    if help is None or not help.body:
        return ""

    from builder.models.widgets.expanding_textbox import ExpandingTextbox

    textbox = (
        ExpandingTextbox(title=help.title, body=help.body)
        if help.title is not None
        else ExpandingTextbox(body=help.body)
    )
    return f"\n{textbox.to_html()}"


