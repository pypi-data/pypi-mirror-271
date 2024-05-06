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


def parallel(
    generator: Iterable[Callable[[], Any]] | list[Callable[[], Any]],
    workers: int | None = None,
    total: int | None = None,
    progress: bool = True,
) -> list:
    from concurrent.futures import ThreadPoolExecutor

    if isinstance(generator, list):
        total = len(generator)

    if progress:
        generator = tqdm(generator, total=total)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(lambda x: x(), generator))
