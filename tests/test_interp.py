import numpy as np
from asce7.interp import _twice_interp1d_with_2d_z,_twice_interp1d_with_2d_x


def test_twice_interp1d_with_2d_z():
    f = _twice_interp1d_with_2d_z(np.array([1,2]), np.array([1,2,3]), np.array([[1,2,3],[4,5,6]]), x_axis=0, bounds_error=False, fill_value=None)
    assert f(1.5, 1.5) == 3.0
    assert f(1, 1.5) == 1.5
    assert f(1.5, 1) == 2.5


def test_twice_interp1d_with_2d_x():
    f = _twice_interp1d_with_2d_x(np.array([[1,2],[3,4],[5,6]]), np.array([1,2,3]), np.array([1,2]), y_axis=0, bounds_error=False, fill_value=None)
    assert f(1.0, 1.0) == 1.0
    assert f(3.0, 2.0) == 1.0
    assert f(5.0, 3.0) == 1.0
    assert f(1.5, 1.5) == 1.0
