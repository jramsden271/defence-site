from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field, field_validator

if TYPE_CHECKING:
    from models.widgets.expanding_textbox import ExpandingTextbox


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
    from models.basic.p import P

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


def normalise_help(value):
    """Coerce a ``help`` input into a :class:`~models.forms.details.Details`.

    Accepts an existing ``Details`` (used as-is), a single string, or a list of
    strings (each becomes a help paragraph under a default "Help" summary), or
    ``None``. Used as a ``mode="before"`` field validator.
    """
    # Lazy import: Details lives in models.forms and imports from this module.
    from models.widgets.expanding_textbox import ExpandingTextbox

    if value is None or isinstance(value, ExpandingTextbox):
        return value
    if isinstance(value, str):
        value = [value]
    return ExpandingTextbox(body=list(value))


class HasHelp(BaseElement):
    """
    Mixin giving an element an optional collapsible help block.

    ``help`` may be passed as a :class:`~models.forms.details.Details` (for full
    control over the summary/paragraphs) or, as a shortcut, a string or list of
    strings which are turned into a default-"Help"-summary ``Details``.

    Elements render it via :meth:`help_html`, so it is up to each element to
    decide *where* the help appears in its own markup.
    """

    # Accepts a ExpandingTextbox, a string, or a list of strings; the validator below
    # normalises all of these to a ExpandingTextbox (or None).
    help: "ExpandingTextbox | str | list[str] | None" = Field(
        default=None, description="Optional help: a ExpandingTextbox, or string(s) shortcut."
    )

    _normalise_help = field_validator("help", mode="before")(normalise_help)

    def help_html(self) -> str:
        """Rendered help HTML (prefixed with a newline), or "" if no help set.

        The validator has already coerced ``help`` to a ``ExpandingTextbox`` (or None);
        the isinstance check just makes that guarantee explicit to type checkers.
        """
        if isinstance(self.help, ExpandingTextbox):
            return f"\n{self.help.to_html()}"
        return ""

    def add_help(self, title: str = "Help", body: list[str] | str | None = None) -> None:
        """Build a :class:`ExpandingTextbox` from ``summary``/``paragraphs`` and set it as ``help``."""
        if isinstance(body, str):
            body = [body]
        self.help = ExpandingTextbox(body=list(body or []))


# Resolve the ``help: ExpandingTextbox | None`` forward reference now that the module is
# otherwise complete. Imported at the bottom to avoid a circular import: ExpandingTextbox
# depends on BaseElement/P above, not on HasHelp. Doing this here (rather than
# relying on each caller to import ExpandingTextbox first) makes HasHelp usable on its
# own regardless of import order.
from models.widgets.expanding_textbox import ExpandingTextbox  # noqa: E402,F401

HasHelp.model_rebuild()
