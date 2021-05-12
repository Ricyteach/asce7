from asce7.v2016.chapter29 import _fig_29p4d7_GCrn_nom
import pytest


@pytest.fixture(scope='module')
def fig_29p4d7_GCrn_nom():
    return _fig_29p4d7_GCrn_nom()


def test_fig_29p4d7_GCrn_nom(fig_29p4d7_GCrn_nom):
    assert fig_29p4d7_GCrn_nom


@pytest.mark.parametrize('zone, tilt, An, GCrn_nom', [
    (1, 5, 500, 0.35),
])
def test_fig_29p4d7_GCrn_nom_lookup(fig_29p4d7_GCrn_nom, zone, tilt, An, GCrn_nom):
    index = (tilt, An)
    assert fig_29p4d7_GCrn_nom.lookup[zone](*index) == pytest.approx(GCrn_nom)
