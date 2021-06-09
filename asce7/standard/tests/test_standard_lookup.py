import pytest
from asce7.standard import StandardLookup
import pandas as pd


@pytest.fixture
def rows():
    return ["A", "B"]


@pytest.fixture
def subrows():
    return ["1", "2"]


@pytest.fixture
def x():
    return [1, 2]


@pytest.fixture
def y():
    return [10, 20, 30]


@pytest.fixture
def z():
    return [
            # _X=1_    |    _X=2_
        # Y= 10 20  30 | 10  20  30
        # A1
            [ 1, 2,  3,   4,  5,  6],
        # A2
            [ 2, 4,  6,   8, 10, 12],
        # B1
            [ 3, 6,  9,  12, 15, 18],
        # B2
            [ 4, 8, 12,  16, 20, 24],
        ]


@pytest.fixture
def index(rows, subrows):
    return pd.MultiIndex.from_product([rows, subrows])


@pytest.fixture
def xy_standard(x, y, z, index):
    return StandardLookup(x, y, z, index=index)


def test_init(xy_standard):
    assert xy_standard


def test_repr(xy_standard):
    r = repr(xy_standard)
    assert r


def test_lookup(xy_standard):
    assert xy_standard.lookup[("B", "1")](1.5, 25) == 16
