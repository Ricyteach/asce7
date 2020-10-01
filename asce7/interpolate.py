"""Interpolation helpers"""


class InterpolationError(Exception):
    pass


class LengthError(Exception):
    pass


def length_match_guard(*collections):
    """Check is collections are the same length"""
    if len({len(c) for c in collections}) != 1:
        raise LengthError("length mismatch")


def linearly_interpolate(v, x1, x2, y1, y2):
    """Linearly interpolate along a two point line"""
    return y1 + (v - x1) * (y2 - y1) / (x2 - x1)


def linear_interpolator(x1, x2, y1, y2):
    """Create an interpolating function using the provided xs and ys"""

    def interpolator(v):
        return linearly_interpolate(v, x1, x2, y1, y2)

    return interpolator


def piecewise_index(v, numbers):
    """Find first index where v is the middle value"""
    try:
        return next(
            i
            for i, (n1, n2) in enumerate(zip(numbers[:-1], numbers[1:]))
            if sorted([v, n1, n2])[1] == v
        )
    except StopIteration:
        raise InterpolationError("Value does not fall in any of the ranges")


def piecewise_line_coordinates_from_index(idx, x1s, x2s, y1s, y2s):
    """Find the x and y coordinates that define the proper piecewise line
    in a set of curves for at the provided index, idx
    """
    x1, x2, y1, y2 = next(
        tup for i, tup in enumerate(zip(x1s, x2s, y1s, y2s)) if i == idx
    )
    return x1, x2, y1, y2


def piecewise_line_coordinates_from_value(v, xs, ys):
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


def piecewise_interpolate(v, xs, ys):
    """Linearly interpolate across piecewise curves"""
    return linearly_interpolate(v, *piecewise_line_coordinates_from_value(v, xs, ys))


def piecewise_interpolator(xs, ys):
    """Create an interpolating function across piecewise curves using the provided xs and ys"""
    try:
        length_match_guard(xs, ys)
    except LengthError as e:
        raise InterpolationError("xs and ys must be of same length") from e
    x1s, x2s, y1s, y2s = xs[:-1], xs[1:], ys[:-1], ys[1:]
    piecewise_section_coordinates = list(zip(x1s, x2s, y1s, y2s))
    interpolators = [linear_interpolator(*tup) for tup in piecewise_section_coordinates]

    def interpolate(v):
        idx = piecewise_index(v, xs)
        interpolator = interpolators[idx]
        return interpolator(v)

    return interpolate
