"""
Loads a page's help text from a JSON file.

Help text is page content, not code, so it lives in the page's own folder
(e.g. ``pages/no_stopping_defence/help_text.json``) rather than in a Python
module here. This loader is the only thing that needs to know how that JSON
maps onto :class:`~models.questions.base_question.HelpText`.
"""

import json
from pathlib import Path

from builder.models.questions.base_question import HelpText


def load_help_text(path: Path) -> dict[str, HelpText]:
    """Load a help-text JSON file into ``{key: HelpText(title, body)}``.

    Each JSON object entry must have ``title`` (string or ``null``) and
    ``body`` (string) keys, matching :class:`HelpText`'s fields. Each entry is
    validated via pydantic, so a malformed entry (wrong type, missing/extra
    key) fails immediately here with a clear error, rather than surfacing
    later as a confusing rendering bug. Look up an entry by its key and pass
    it to a question's ``set_help()``, e.g.::

        help_text = load_help_text(page_dir / "help_text.json")
        some_question.set_help(help_text["pronouns_why"])
    """
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {key: HelpText.model_validate(entry) for key, entry in raw.items()}
