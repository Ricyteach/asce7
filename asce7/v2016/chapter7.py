"""ASCE 7 Figures"""

from ..exceptions import ASCE7Error


def _fig_7_pt_4_dsh_1(C_t, roof_slope_deg):
    """For determining C_s"""


def _get_figure(C_t):
    """Retrieve correct subfigure for C_s"""
    if C_t >= 1.2:
        return _fig_7_dsh_2c
    elif C_t == 1.1:
        return _fig_7_dsh_2b
    elif C_t <= 1.0:
        return _fig_7_dsh_2a
    else:
        raise ASCE7Error(f"{C_s=:.1f} is unsupported in ASCE 7")


def _fig_7_dsh_2a(roof_slope_deg):
    """Retrieve value for C_t<=1.0"""
    _fig_7_dsh_2a_interpolator(roof_slope_deg)
    return interpolate()
