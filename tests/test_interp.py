import pytest
import numpy as np
from asce7.interp import interp1d_twice
from asce7.common import Log


@pytest.mark.parametrize("x, y, z", [
    (1.5, 1.5, 3.0),
    (1, 1.5, 1.5),
    (1.5, 1, 2.5),
])
def test_twice_interp1d_with_2d_z(x, y, z):
    f = interp1d_twice(np.array([1, 2]), np.array([1, 2, 3]), np.array([[1, 2, 3],
                                                                        [4, 5, 6]]),
                       axis=0, bounds_error=True, fill_value=None)
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
    I hope not because it will be a real PITA.
    See:
    https://github.com/scipy/scipy/issues/14735
    """
    f = interp1d_twice(np.array([[1, 2],
                                 [3, 4],
                                 [5, 6]]), np.array([1, 2, 3]), np.array([1, 2]),
                       axis=0, bounds_error=False, fill_value=None)
    assert f(x, y) == z


@pytest.fixture(scope="session")
def FIG7P4D1_Cs_data():
    x_arr = [[0, 5, 70, 90],
             [0, 10, 70, 90],
             [0, 15, 70, 90]]
    y_arr = [1.0, 1.1, 1.2]
    z_arr = [1.0, 1.0, 0, 0]
    return (x_arr, y_arr, z_arr)


@pytest.fixture(scope="session", params=[
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
def FIG7P4D1_Cs_interpolations_xyz(request):
    return request.param


@pytest.fixture
def interp1d_twice_with_2d_x_FIG7P4D1_Cs(FIG7P4D1_Cs_data):
    x_arr, y_arr, z_arr = FIG7P4D1_Cs_data
    return interp1d_twice(x_arr, y_arr, z_arr, 0, True, None)


@pytest.fixture(scope="session", )
def FIG29P4D7_GCrn_nom_Zone_1_data():
    x_arr = [Log(1), Log(500), Log(5000)]
    y_arr = [0, 5, 15, 35]
    z_arr = [[1.5, 0.35, 0.10],
             [1.5, 0.35, 0.10],
             [2.0, 0.56, 0.30],
             [2.0, 0.56, 0.30]]
    return (x_arr, y_arr, z_arr)


@pytest.fixture(scope="session", params=[
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
def FIG29P4D7_GCrn_nom_Zone_1_interpolations_xyz(request):
    return request.param


@pytest.fixture
def interp1d_twice_with_2d_z_FIG29P4D7_GCrn_nom_Zone_1(FIG29P4D7_GCrn_nom_Zone_1_data):
    x_arr, y_arr, z_arr = FIG29P4D7_GCrn_nom_Zone_1_data
    return interp1d_twice(x_arr, y_arr, z_arr, 1, True, None)


def test_FIG7P4D1_Cs(FIG7P4D1_Cs_interpolations_xyz, interp1d_twice_with_2d_x_FIG7P4D1_Cs):
    x, y, expected = FIG7P4D1_Cs_interpolations_xyz
    result = interp1d_twice_with_2d_x_FIG7P4D1_Cs(x, y)
    np.testing.assert_array_equal(result, expected)


def test_FIG29P4D7_GCrn_nom_Zone_1(FIG29P4D7_GCrn_nom_Zone_1_interpolations_xyz,
                                   interp1d_twice_with_2d_z_FIG29P4D7_GCrn_nom_Zone_1):
    x, y, expected = FIG29P4D7_GCrn_nom_Zone_1_interpolations_xyz
    result = interp1d_twice_with_2d_z_FIG29P4D7_GCrn_nom_Zone_1(x, y)
    np.testing.assert_array_almost_equal(result, expected, decimal=16)
