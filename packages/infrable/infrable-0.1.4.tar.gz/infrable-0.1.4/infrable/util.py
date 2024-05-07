from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from typing import Any, Callable, Iterable

from jinja2 import Template
from tqdm import tqdm


def formatter(template: str) -> Template:
    return Template(
        template,
        variable_start_string="{",
        variable_end_string="}",
        autoescape=False,
        keep_trailing_newline=True,
        finalize=lambda x: x or "",
    )


@contextmanager
def parallelcontext(
    generator: Iterable[Callable[[], Any]] | list[Callable[[], Any]],
    workers: int | None = None,
    total: int | None = None,
    progress: bool = True,
):
    """Context manager, run a list of functions in parallel."""

    if progress:
        generator = tqdm(generator, total=total)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        yield executor.map(lambda x: x(), generator)


def parallel(
    generator: Iterable[Callable[[], Any]] | list[Callable[[], Any]],
    workers: int | None = None,
    total: int | None = None,
    progress: bool = True,
) -> list:
    """Run a list of functions in parallel."""

    with parallelcontext(
        generator, workers=workers, total=total, progress=progress
    ) as results:
        return list(results)
