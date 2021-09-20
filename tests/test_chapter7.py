from asce7.common import Deg, SlopeIn12
from asce7.v2016.chapter7 import fig7p4d1_Cs
import pytest


@pytest.mark.parametrize('surface_type, roof_slope, temp_coefficient, Cs', [
    ("slippery", Deg(5), 1.0, 1.0),
    ("slippery", SlopeIn12(4), 1.0, 0.7933),
])
def test_fig7p4d1_Cs(surface_type, temp_coefficient, roof_slope, Cs):
    assert fig7p4d1_Cs(surface_type, roof_slope, temp_coefficient) == pytest.approx(Cs, abs=0.0001)
