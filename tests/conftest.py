import pytest
import asce7.v2016 as asce7


@pytest.fixture
def risk(request):
    return asce7.Risk[request.param].value


@pytest.fixture(params=list(asce7.Risk))
def all_risk(request):
    return asce7.Risk[request.param].value


@pytest.fixture
def load_type(request):
    return asce7.LoadType[request.param].value
