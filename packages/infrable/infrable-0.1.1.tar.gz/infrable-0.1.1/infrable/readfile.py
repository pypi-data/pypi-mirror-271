from pathlib import Path
from typing import Callable


def readfile(
    path: Path | str,
    init: Callable[[], str] = str,
    fmt: Callable[[str], str] | None = lambda s: s.strip(),
) -> str:
    """Get the contents of a file, creating it if it doesn't exist."""

    if isinstance(path, str):
        path = Path(path)
    if not path.exists():
        val = init()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(val)
    else:
        val = path.read_text()
    if fmt:
        return fmt(val)
    return val
