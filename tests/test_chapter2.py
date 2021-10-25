import pytest
import numpy as np
from asce7.v2016.chapter2 import Strength, ASD


@pytest.mark.parametrize("D", [
    1,
    np.array([1, 2])
])
def test_strength(D):
    s = Strength()
    W = 2
    result = s.wind_up_load(D, W)
    np.testing.assert_almost_equal(result, 0.9*D + W)


@pytest.mark.parametrize("D", [
    1,
    np.array([1, 2])
])
def test_asd(D):
    a = ASD()
    W = 2
    result = a.wind_up_load(D, W)
    np.testing.assert_almost_equal(result, 0.6*D + 0.6*W)
