import pytest
import asce7.v2016 as asce7

def test_Is(all_risk):
    assert asce7.I_s(all_risk)

def test_Ie(all_risk):
    assert asce7.I_e(all_risk)
