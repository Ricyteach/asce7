import pytest
from asce7.common import Log
from ceng.interp import interp1d_twice
import numpy as np


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


def test_FIG29P4D7_GCrn_nom_Zone_1(FIG29P4D7_GCrn_nom_Zone_1_interpolations_xyz,
                                   interp1d_twice_with_2d_z_FIG29P4D7_GCrn_nom_Zone_1):
    x, y, expected = FIG29P4D7_GCrn_nom_Zone_1_interpolations_xyz
    result = interp1d_twice_with_2d_z_FIG29P4D7_GCrn_nom_Zone_1(x, y)
    np.testing.assert_array_almost_equal(result, expected, decimal=16)
