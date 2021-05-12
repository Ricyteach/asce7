import pytest

import asce7.v2016 as asce7
snow = asce7.snow
seismic = asce7.seismic

@pytest.fixture(params=["I", "II", "III", "IV"])
def risk(request):
    return asce7.RiskCategory[request.param]


@pytest.mark.parametrize("load_type", [
    "S", "E"
])
def test_importance_factor(load_type, risk):
    assert asce7.importance_factor(load_type)(risk)

def test_Is(risk):
    assert asce7.I_s(risk)

def test_Ie(risk):
    assert asce7.I_e(risk)
