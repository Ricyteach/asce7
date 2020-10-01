import pytest
from pytest import approx
import asce7.interpolate as terp

INTERPOLATIONS = [
    (1, 0, 2, 0.2, 0.1, 0.15),
    (0.001, 0, 0.002, 0.2, 0.1, 0.15),
]


PIECEWISE_INTERPOLATIONS = [
    (3.0, [2.0, 4.0, 6.0, 8.0], [1.0, 3.0, 5.0, 7.0], 2.0),
]


@pytest.mark.parametrize("v, x1, x2, y1, y2, expected", INTERPOLATIONS)
def test_linear_interpolate(v, x1, x2, y1, y2, expected):
    assert terp.linearly_interpolate(v, x1, x2, y1, y2) == approx(expected)


@pytest.mark.parametrize("v, x1, x2, y1, y2, expected", INTERPOLATIONS)
def test_linear_interpolator(v, x1, x2, y1, y2, expected):
    interpolator = terp.linear_interpolator(x1, x2, y1, y2)
    result = interpolator(v)
    assert result == approx(expected)


@pytest.mark.parametrize(
    "v, numbers, index",
    [
        (1.1, [-1.1, -0.5, 0.25, 0.9, 1.2], 3),
        (0.9, [-1.1, -0.5, 0.25, 0.9, 1.2], 2),
    ],
)
def test_piecewise_index(v, numbers, index):
    result = terp.piecewise_index(v, numbers)
    assert result == index


@pytest.mark.parametrize(
    "idx, xs, ys, tup",
    [
        (2, [2.0, 4.0, 6.0, 8.0], [1.0, 3.0, 5.0, 7.0], (6.0, 8.0, 5.0, 7.0)),
    ],
)
def test_piecewise_line_coordinates_from_index(idx, xs, ys, tup):
    result = terp.piecewise_line_coordinates_from_index(idx, xs, xs[1:], ys, ys[1:])
    assert result == approx(tup)


@pytest.mark.parametrize(
    "v, xs, ys, tup",
    [
        (7.0, [2.0, 4.0, 6.0, 8.0], [1.0, 3.0, 5.0, 7.0], (6.0, 8.0, 5.0, 7.0)),
    ],
)
def test_piecewise_line_coordinates_from_value(v, xs, ys, tup):
    result = terp.piecewise_line_coordinates_from_value(v, xs, ys)
    assert result == approx(tup)


@pytest.mark.parametrize("v, xs, ys, expected", PIECEWISE_INTERPOLATIONS)
def test_piecewise_interpolate(v, xs, ys, expected):
    result = terp.piecewise_interpolate(v, xs, ys)
    assert result == approx(expected)


@pytest.mark.parametrize("v, xs, ys, expected", PIECEWISE_INTERPOLATIONS)
def test_piecewise_interpolator(v, xs, ys, expected):
    interpolator = terp.piecewise_interpolator(xs, ys)
    result = interpolator(v)
    assert result == approx(expected)
