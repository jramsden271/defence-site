from pathlib import Path

from pydantic import BaseModel, Field, model_validator


class Resource(BaseModel):
    """
    A single static asset (CSS, JS, or media file) contributed by a
    :class:`~builder.models.component.Component`, on its way to being
    bundled into a page's output.

    Either ``source_path`` (an existing file to copy/read) or
    ``content`` (already-generated text, e.g. a field manifest built
    from a form at build time — see
    :mod:`~builder.field_manifest`) must be set, not both. ``dest_name``
    is this resource's filename in whatever it gets bundled into; for
    a ``source_path`` resource it defaults to ``source_path.name``, and
    is required for a ``content`` resource (there's no filename to
    default from).
    """

    source_path: Path | None = None
    content: str | None = None
    dest_name: str | None = Field(
        default=None, description="Output filename; defaults to source_path.name for file-backed resources."
    )

    @model_validator(mode="after")
    def _check_exactly_one_source(self) -> "Resource":
        if (self.source_path is None) == (self.content is None):
            raise ValueError("Resource requires exactly one of source_path or content.")
        if self.content is not None and self.dest_name is None:
            raise ValueError("Resource(content=...) requires dest_name.")
        return self

    def resolved_dest_name(self) -> str:
        return self.dest_name or self.source_path.name

    def read_text(self, encoding: str = "utf-8") -> str:
        """This resource's text content, whether it came from
        ``content`` directly or is read from ``source_path``."""
        if self.content is not None:
            return self.content
        return self.source_path.read_text(encoding=encoding)

    def read_bytes(self) -> bytes:
        """This resource's raw bytes, for a binary (media) resource."""
        if self.content is not None:
            return self.content.encode("utf-8")
        return self.source_path.read_bytes()

    def dedup_key(self) -> "Path | tuple[str, str]":
        """A hashable identity for deduplication: the source file's path
        for a file-backed resource, or the ``(dest_name, content)`` pair
        for a generated one (no path to key off)."""
        return self.source_path if self.source_path is not None else (self.dest_name, self.content)


class ResourceBundle(BaseModel):
    """
    The flat, deduplicated set of resources gathered from a component
    tree via :meth:`~builder.models.component.Component.gather_resources`:
    every CSS file to be concatenated into the page's stylesheet, every
    JS file to be concatenated into the page's script, and every media
    file to be copied alongside it.

    Dedup is by source identity (see :meth:`Resource.dedup_key`) — a
    shared component included twice in the same tree (e.g. a widget
    used by two form fields) contributes its resources only once.
    """

    css: list[Resource] = Field(default_factory=list)
    js: list[Resource] = Field(default_factory=list)
    media: list[Resource] = Field(default_factory=list)

    def merge(self, other: "ResourceBundle") -> "ResourceBundle":
        """Return a new bundle combining ``self`` and ``other``, with
        duplicate resources (within each category) dropped."""
        return ResourceBundle(
            css=_dedup(self.css + other.css),
            js=_dedup(self.js + other.js),
            media=_dedup(self.media + other.media),
        )


def _dedup(resources: list[Resource]) -> list[Resource]:
    seen: set = set()
    result = []
    for resource in resources:
        key = resource.dedup_key()
        if key in seen:
            continue
        seen.add(key)
        result.append(resource)
    return result
