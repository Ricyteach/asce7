import pytest
import numpy as np
from asce7.interp import _twice_interp1d_with_2d_z,_twice_interp1d_with_2d_x
from asce7.common import Log


@pytest.mark.parametrize("x, y, z", [
    (1.5, 1.5, 3.0),
    (1, 1.5, 1.5),
    (1.5, 1, 2.5),
])
def test_twice_interp1d_with_2d_z(x, y, z):
    f = _twice_interp1d_with_2d_z(np.array([1,2]), np.array([1,2,3]), np.array([[1,2,3],
                                                                                [4,5,6]]),
                                  x_axis=0, bounds_error=True, fill_value=None)
    assert f(x, y) == z


@pytest.mark.skip(reason="YAGNI?")
@pytest.mark.parametrize("x, y, z", [
    (1.0, 1.0, 1.0),
    (3.0, 2.0, 1.0),
    (5.0, 3.0, 1.0),
    (1.5, 1.5, 1.0),
])
def test_twice_interp1d_with_2d_x(x, y, z):
    """This is a test that might be required to pass in the future if ever a chart/table comes up demanding it.
    I hope not because it will be a real PIA.
    See:
    https://github.com/scipy/scipy/issues/14735
    """
    f = _twice_interp1d_with_2d_x(np.array([[1,2],
                                            [3,4],
                                            [5,6]]), np.array([1,2,3]), np.array([1,2]),
                                  y_axis=0, bounds_error=True, fill_value=None)
    assert f(x, y) == z


@pytest.fixture
def interp1d_with_2d_x_FIG7P4D1_Cs():
    x_arr = np.array([[0, 5, 70, 90],
             [0, 10, 70, 90],
             [0, 15, 70, 90]])
    y_arr = np.array([1.0, 1.1, 1.2])
    z_arr = np.array([1.0, 1.0, 0, 0])
    return _twice_interp1d_with_2d_x(x_arr, y_arr, z_arr, 0, True, None)


@pytest.fixture
def interp1d_with_2d_z_FIG29P4D7_GCrn_nom_Zone_1():
    x_arr = np.array([Log(1), Log(500), Log(5000)])
    y_arr = np.array([0, 5, 15, 35])
    z_arr = np.array([[1.5, 0.35, 0.10], [1.5, 0.35, 0.10], [2.0, 0.56, 0.30], [2.0, 0.56, 0.30]])
    return _twice_interp1d_with_2d_z(x_arr, y_arr, z_arr, 1, True, None)


@pytest.mark.parametrize("x, y, expected", [
    (0, 1.0, 1.0),
    (5, 1.0, 1.0),
    (70, 1.0, 0),
    (90, 1.0, 0),
    (0, 1.1, 1.0),
    (10, 1.1, 1.0),
    (70, 1.1, 0),
    (90, 1.1, 0),
    (0, 1.2, 1.0),
    (15, 1.2, 1.0),
    (70, 1.2, 0),
    (90, 1.2, 0),

    (1, 1.0, 1.0),
    (37.5, 1.0, 0.5),
    (80, 1.0, 0),
    (1, 1.1, 1.0),
    (40, 1.1, 0.5),
    (80, 1.1, 0),
    (1, 1.2, 1.0),
    (42.5, 1.2, 0.5),
    (80, 1.2, 0),
])
def test_FIG7P4D1_Cs(x, y, expected, interp1d_with_2d_x_FIG7P4D1_Cs):
    result = interp1d_with_2d_x_FIG7P4D1_Cs(x, y)
    np.testing.assert_array_equal(result, expected)


@pytest.mark.parametrize("x, y, expected", [
    (Log(1), 0, 1.5),
    (Log(1), 5, 1.5),
    (Log(1), 15, 2.0),
    (Log(1), 35, 2.0),
    (Log(500), 0, 0.35),
    (Log(500), 5, 0.35),
    (Log(500), 15, 0.56),
    (Log(500), 35, 0.56),
    (Log(5000), 0, 0.10),
    (Log(5000), 5, 0.10),
    (Log(5000), 15, 0.30),
    (Log(5000), 35, 0.30),
])
def test_FIG29P4D7_GCrn_nom_Zone_1(x, y, expected, interp1d_with_2d_z_FIG29P4D7_GCrn_nom_Zone_1):
    result = interp1d_with_2d_z_FIG29P4D7_GCrn_nom_Zone_1(x, y)
    np.testing.assert_array_almost_equal(result, expected, decimal=16)
