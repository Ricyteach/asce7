from asce7.common import Deg, SlopeIn12
from asce7.v2016.chapter7 import fig7p4d1_Cs
from ceng.interp import interp1d_twice
import numpy as np
import pytest


@pytest.mark.parametrize('surface_type, roof_slope, temp_coefficient, Cs', [
    ("slippery", Deg(5), 1.0, 1.0),
    ("slippery", SlopeIn12(4), 1.0, 0.7933),
])
def test_fig7p4d1_Cs(surface_type, temp_coefficient, roof_slope, Cs):
    assert fig7p4d1_Cs(surface_type, roof_slope, temp_coefficient) == pytest.approx(Cs, abs=0.0001)


@pytest.fixture(scope="session")
def FIG7P4D1_Cs_data():
    x_arr = [[0, 5, 70, 90],
             [0, 10, 70, 90],
             [0, 15, 70, 90]]
    y_arr = [1.0, 1.1, 1.2]
    z_arr = [1.0, 1.0, 0, 0]
    return x_arr, y_arr, z_arr


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


def test_FIG7P4D1_Cs(FIG7P4D1_Cs_interpolations_xyz, interp1d_twice_with_2d_x_FIG7P4D1_Cs):
    x, y, expected = FIG7P4D1_Cs_interpolations_xyz
    result = interp1d_twice_with_2d_x_FIG7P4D1_Cs(x, y)
    np.testing.assert_array_equal(result, expected)
