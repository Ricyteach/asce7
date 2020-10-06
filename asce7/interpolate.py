"""Interpolation helpers"""
from decimal import Decimal
from numbers import Real
from typing import Sequence, Callable, Union, Sized, Iterable, TypeVar

T = TypeVar("T", Real, Decimal, float)


class InterpolationError(Exception):
    pass


class LengthError(Exception):
    pass


def length_match_guard(*collections: Sized) -> None:
    """Check is collections are the same length"""
    if len({len(c) for c in collections}) != 1:
        raise LengthError("length mismatch")


def linearly_interpolate(v: T, x1: T, x2: T, y1: T, y2: T) -> T:
    """Linearly interpolate along a two point line"""
    return y1 + (v - x1) * (y2 - y1) / (x2 - x1)


def linear_interpolator(
    x1: T, x2: T, y1: T, y2: T
) -> Callable[[T], T]:
    """Create an interpolating function using the provided xs and ys"""

    def interpolator(v: T) -> T:
        return linearly_interpolate(v, x1, x2, y1, y2)

    return interpolator


def piecewise_index(v: T, numbers: Sequence[T]) -> int:
    """Find first index where v is the middle value"""
    try:
        return next(
            i
            for i, (n1, n2) in enumerate(zip(numbers[:-1], numbers[1:]))
            if sorted([v, n1, n2])[1] == v
        )
    except StopIteration:
        raise InterpolationError("Value does not fall in any of the ranges")


def piecewise_line_coordinates_from_index(
    idx: int, x1s: Iterable[T], x2s: Iterable[T], y1s: Iterable[T], y2s: Iterable[T]
) -> tuple[T, T, T, T]:
    """The x and y coordinates that define the proper piecewise line
    in a set of curves at the provided index, idx
    """
    x1, x2, y1, y2 = next(
        tup for i, tup in enumerate(zip(x1s, x2s, y1s, y2s)) if i == idx
    )
    return x1, x2, y1, y2


def piecewise_line_coordinates_from_value(v: T, xs: Sequence[T], ys: Sequence[T]) -> tuple[T, T, T, T]:
    """Find the x and y coordinates that define the proper piecewise line in a set of curves
    for the provided value, v
    """
    try:
        length_match_guard(xs, ys)
    except LengthError as e:
        raise InterpolationError("xs and ys must be of same length") from e
    # find xs index where v is the middle value
    idx = piecewise_index(v, xs)
    x1, x2, y1, y2 = piecewise_line_coordinates_from_index(
        idx, xs[:-1], xs[1:], ys[:-1], ys[1:]
    )
    return x1, x2, y1, y2


def piecewise_interpolate(v: T, xs: Sequence[T], ys: Sequence[T]):
    """Linearly interpolate across piecewise curves"""
    return linearly_interpolate(v, *piecewise_line_coordinates_from_value(v, xs, ys))


def piecewise_interpolator(xs: Sequence[T], ys: Sequence[T]) -> Callable[[T], T]:
    """Create an interpolating function across piecewise curves using the provided xs and ys"""
    try:
        length_match_guard(xs, ys)
    except LengthError as e:
        raise InterpolationError("xs and ys must be of same length") from e
    x1s, x2s, y1s, y2s = xs[:-1], xs[1:], ys[:-1], ys[1:]
    piecewise_section_coordinates = list(zip(x1s, x2s, y1s, y2s))
    interpolators = [linear_interpolator(*tup) for tup in piecewise_section_coordinates]

    def interpolate(v: T) -> T:
        idx = piecewise_index(v, xs)
        interpolator = interpolators[idx]
        return interpolator(v)

    return interpolate
