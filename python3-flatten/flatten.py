from typing import Any, Iterable


def isiterable(src) -> bool:
    if type(src) == str:
        return False
    return hasattr(src, "__iter__") and callable(src.__iter__)


def iterflatten(src: Iterable[Any | Iterable]) -> Iterable:
    for datum in src:
        if isiterable(datum):
            yield from iterflatten(datum)
        else:
            yield datum


def flatten(src: Iterable[Any | Iterable]) -> tuple:
    return tuple(iterflatten(src))
