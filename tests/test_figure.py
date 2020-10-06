from asce7.figure import Figure
import pytest


@pytest.mark.parametrize("figure, r_str", [
    (Figure(), "Figure()"),
    (Figure(a=([], [])), "Figure(a=([], []))"),
])
def test_figure_repr(figure, r_str):
    assert repr(figure) == r_str
