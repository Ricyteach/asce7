import pytest
from asce7.v2016.chapter1 import importance_factor


@pytest.mark.parametrize("load_type", [
    "S", "E", "Di"
], indirect=True)
def test_importance_factor(all_risk, load_type):
    assert importance_factor(all_risk, load_type)
