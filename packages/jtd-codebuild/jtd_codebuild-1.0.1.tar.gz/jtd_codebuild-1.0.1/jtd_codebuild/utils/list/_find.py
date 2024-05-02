from typing import TypeVar, Callable
from toolz import pipe
from toolz.curried import filter

T = TypeVar("T")


def find(
    predicate: Callable[[T], bool],
    nodes: list[T],
) -> list[T]:
    return pipe(
        nodes,
        filter(predicate),
        list,
    )


def find_one(
    predicate: Callable[[T], bool],
    nodes: list[T],
) -> T | None:
    found = find(predicate, nodes)
    if len(found) > 0:
        return found[0]
    return None
