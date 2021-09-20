from asce7.v2016.chapter29 import fig29p4d7_GCrn_nom
import pytest


@pytest.mark.parametrize('zone, tilt, An, GCrn_nom', [
    ("1", 5, 500, 0.35),
])
def test_fig29p4d7_GCrn_nom(zone, tilt, An, GCrn_nom):
    assert fig29p4d7_GCrn_nom(zone, tilt, An) == pytest.approx(GCrn_nom)
