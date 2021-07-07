"""ASCE 7 Figures"""

from asce7.lookup import ParameterStandard


_FIG7P4D1_Cs__STR = """
        Surface Type
        slippery        other

C_t     roof slope (deg)
1.0     5       70      30      70
1.1     10      70      37.5    70
1.2     15      70      45      70

C_s     1.0      0      1.0     0
""".replace("    ", "\t")


def _fig7p4d1_Cs():
    """Figure 29.4-7: Design Wind Loads (All Heights): Rooftop Solar Panels for Enclosed and Partially Enclosed
    Buildings, Roof θ≤7°

    Nominal Net Pressure Coefficients (Gcrn)nom
    """
    seq = [value.strip() for line in _FIG7P4D1_Cs__STR[1:-1].split("\n") for value in line.strip().split(" " * 4)]
    labels = {seq[0][0]: seq[1]}  # surface type
    indexes = {
        seq[4][0]: [float(row[0]) for row in seq[5:]],  # temperature coefficient, C_t
        seq[4][1]: [[eval(v) for v in row[1:]] for row in seq[5:]],  # roof slope (deg) tuples
    }
    dependent_axis = {seq[2][1]: [eval(v) for v in seq[3]]}  # C_s

    return ParameterStandard(dependent_axis, indexes, labels)


def _fig7p3d2a(roof_slope_deg):
    """Retrieve value for C_t<=1.0"""
    _fig_7_dsh_2a_interpolator(roof_slope_deg)
    return interpolate()
