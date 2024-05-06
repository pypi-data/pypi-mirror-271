from dataclasses import asdict, dataclass, field
from typing import Any

from typer import Typer

from infrable import errors, paths
from infrable.meta import Meta
from infrable.util import formatter


@dataclass(unsafe_hash=True, order=True, eq=True)
class Switch:
    """A switch for the infrastructure."""

    options: set[str]
    init: str

    typer: Typer | None = None
    meta: Meta = field(default_factory=Meta)

    def __post_init__(self):
        self.path = paths.switches / "-".join(sorted(self.options))
        if not self.path.exists():
            self.set(self.init)

    def __call__(self, **cases: Any) -> Any:
        if not cases:
            cases = {opt: opt for opt in self.options}
        elif set(cases.keys()) != self.options:
            raise errors.SwitchCaseError(self.path, options=self.options, cases=cases)

        val = self.path.read_text().strip()
        if val in cases:
            return cases[val]

        raise errors.SwitchError(self.path, val=val, cases=cases)

    def set(self, value: str):
        if value in self.options:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(value)
            return

        self.path.unlink(missing_ok=True)
        raise errors.SwitchValueError(self.path, value=value, options=self.options)

    def format(self, name: str, format) -> str:
        return formatter(format).render(name=name, **asdict(self))

    def __str__(self) -> str:
        return self()
