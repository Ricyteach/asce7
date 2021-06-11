"""Utility module for checking internal equality of Collections."""
import itertools
from typing import NamedTuple, TypeVar, Iterator, Collection, Union

T = TypeVar("T")


class _NotEqual:
    def __repr__(self):
        return "_NOTEQUAL"


_NOTEQUAL = _NotEqual()


class _Empty:
    def __repr__(self):
        return "_EMPTY"


_EMPTY = _Empty()


class AllEqualResult(NamedTuple):
    value: T
    iterator: Iterator[T]

    def __bool__(self):
        return self.value is not _NOTEQUAL


def all_equal(iterable: Collection[T]) -> AllEqualResult[Union[T, _NotEqual, _Empty], Iterator[T]]:
    """Returns an appropriately truthy or falsey AllEqualResult."""

    g = itertools.groupby(iterable)
    result = next(g, True)
    if result and next(g, None) is None:
        if result is not True:
            return AllEqualResult(result[0], iter(iterable))
        else:
            return AllEqualResult(_EMPTY, iter(iterable))
    return AllEqualResult(_NOTEQUAL, iter(()))
