"""ASCE 7 Figures"""

from asce7.lookup import ParameterStandard


def _fig7p4d1():
    """Figure 29.4-7: Design Wind Loads (All Heights): Rooftop Solar Panels for Enclosed and Partially Enclosed
    Buildings, Roof θ≤7°

    Nominal Net Pressure Coefficients (Gcrn)nom
    """
    fig7p4d1_labels = {'Surface Type': ['slippery', 'other']}
    fig7p4d1_indexes = {
        'C_t': (1.0, 1.1, 1.2),  # temperature coefficient
        'roof slope': [[[5, 70],[30, 70],],  # C_t = 1.0 chart
                       [[10, 70],[37.5, 70],],  # C_t = 1.1 chart
                       [[15, 70],[45, 70],],],  # C_t = 1.2 chart
    }
    fig7p4d1_dependent_axis = {
        'C_t = 1.0 chart': [
            [1.0, 0], [1.0, 0],
        ],
        'C_t = 1.1 chart': [
            [1.0, 0], [1.0, 0],
        ],
        'C_t = 1.2 chart': [
            [1.0, 0], [1.0, 0],
        ],
    }

    return ParameterStandard(fig7p4d1_dependent_axis, fig7p4d1_indexes, fig7p4d1_labels)


def _fig7p3d2a(roof_slope_deg):
    """Retrieve value for C_t<=1.0"""
    _fig_7_dsh_2a_interpolator(roof_slope_deg)
    return interpolate()
