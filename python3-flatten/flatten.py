from typing import Any, Iterable
import logging


def iterable(src) -> bool:
    return type(src) in (list, tuple) or hasattr(src, "__iter__")


def flatteniter(src: Iterable[Any | Iterable]) -> Iterable:
    for datum in src:
        if iterable(datum):
            yield from flatteniter(datum)
        else:
            yield datum


def flatten(src: Iterable[Any | Iterable]) -> tuple:
    return tuple(flatteniter(src))
