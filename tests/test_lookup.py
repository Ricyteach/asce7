from asce7.lookup import ParameterStandard
import pytest


@pytest.fixture
def example_1dstandard():
    return ParameterStandard({'chart_label': [[1, 2, 3],[4, 5, 6]]}, {'x':[5, 15, 25]}, {'label': ['a', 'b']})


@pytest.fixture
def example_2dstandard():
    return ParameterStandard({'chart_label p': [[1, 2, 3], [4, 5, 6]],
                              'chart_label q': [[10, 20, 30], [40, 50, 60]]}, {'x':[100, 200],
                                                                               'y':[5, 15, 25]}, {'label': ['a', 'b']})


@pytest.fixture(params=[0, 1])
def example_standard(request, example_1dstandard, example_2dstandard):
    return [example_1dstandard, example_2dstandard][request.param]


def test_parameter_standards(example_standard):
    assert example_standard


@pytest.mark.parametrize('label, x, z', [
    ('a', 10, 1.5),
    ('b', 10, 4.5),
])
def test_parameter_1dlookup(example_1dstandard, label, x, z):
    assert example_1dstandard.lookup[label](x) == pytest.approx(z)


@pytest.mark.parametrize('label, x, y, z', [
    ('a', 100, 10, 1.5),
    ('b', 100, 10, 4.5),
    ('a', 150, 10, (1.5+15)/2),
    ('b', 150, 10, (4.5+45)/2),
    ('a', 200, 10, 15),
    ('b', 200, 10, 45),
])
def test_parameter_2dlookup(example_2dstandard, label, x, y, z):
    assert example_2dstandard.lookup[label](x, y) == pytest.approx(z)
