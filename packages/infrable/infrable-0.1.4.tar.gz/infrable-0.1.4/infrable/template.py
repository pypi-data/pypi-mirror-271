from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml
from jinja2 import StrictUndefined
from jinja2 import Template as JinjaTemplate

from infrable import errors


def _jinja_render(content: str, **ctx) -> str:
    return JinjaTemplate(content, undefined=StrictUndefined).render(**ctx)


@dataclass(frozen=True)
class Dest:
    """Destination for the rendered template, with optional context."""

    loc: str
    chown: Optional[str] = None
    chmod: Optional[str] = None
    ctx: dict = field(default_factory=dict)

    @classmethod
    def parse(cls, data: str | dict):
        """Parse a destination from the given string or dictionary."""

        if isinstance(data, str):
            return cls(loc=data)

        return cls(**data)


@dataclass(frozen=True)
class Metadata:
    """Metadata defined in each template."""

    src: str
    dest: list[Dest]
    chown: Optional[str] = None
    chmod: Optional[str] = None
    skip: bool = False

    _raw: str = ""
    _rendered: str = ""

    @classmethod
    def parse(cls, path: Path, **ctx):
        """Parse metadata from the given file content."""

        reading = False
        raw = ""
        rendered = ""

        for line in path.read_text().splitlines():
            if line == "# ---":
                if reading:
                    break
                else:
                    reading = True
                    continue
            if reading:
                raw += f"{line}\n"

        raw = raw.strip()

        ctx["_template"] = {"src": str(path)}
        rendered = _jinja_render(raw, **ctx)

        yamllines = [line.removeprefix("# ") for line in rendered.splitlines()]
        if not yamllines:
            raise errors.MissingMetadataError(src=path)

        meta: dict = yaml.safe_load("\n".join(yamllines))
        meta_dest: str | dict | list[str | dict] | None = meta.pop("dest")

        if not meta_dest:
            raise errors.MissingDestinationError(src=meta["src"])

        dest = []
        if isinstance(meta_dest, list):
            dest = [Dest.parse(d) for d in meta_dest]
        else:
            dest = [Dest.parse(meta_dest)]

        return cls(dest=dest, _raw=raw, _rendered=rendered, **meta)

    def clean_header(self, dest_loc: str) -> str:
        dest = next(d for d in self.dest if d.loc == dest_loc)

        # We don't need "skip" in the final header
        dict_: dict[str, Any] = {"src": self.src, "dest": dest.loc}

        # We need chown and chmod in the final header to diff file permissions
        chown = dest.chown or self.chown
        if chown:
            dict_["chown"] = str(chown)
        chmod = dest.chmod or self.chmod
        if chmod:
            dict_["chmod"] = str(chmod)

        header = yaml.safe_dump(dict_, default_flow_style=False)
        header = "\n".join(f"# {l}" for l in header.splitlines())
        return header


def render(path: Path, dest_loc: str, **ctx) -> str:
    """Render the template with the given context, for a single destination."""

    meta = Metadata.parse(path, **ctx)
    header = meta.clean_header(dest_loc)
    tmpl = path.read_text().replace(meta._raw, header)
    content = _jinja_render(tmpl, **ctx)

    return f"{content}\n"  # all config, specially sudoers requires a trailing newline
