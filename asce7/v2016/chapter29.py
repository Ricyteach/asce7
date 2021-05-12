import numpy as np
from ..lookup import ParameterStandard

def _fig_29p4d7_GCrn_nom():
    """Figure 29.4-7: Design Wind Loads (All Heights): Rooftop Solar Panels for Enclosed and Partially Enclosed
    Buildings, Roof θ≤7°

    Nominal Net Pressure Coefficients (Gcrn)nom
    """
    fig_29p4d7_labels = {'Zone': [1, 2, 3]}
    fig_29p4d7_indexes = {
                            'tilt (°)': (5, 15),  # degrees
                            'log area (sq ft)': np.log10([1, 500, 5000]),  # log sq ft
                          }
    fig_29p4d7_dependent_axis = {
        '0° to 5° chart': [
            [1.5, 0.35, 0.10],  # curve 0 to 5, Zone 1
            [2.0, 0.45, 0.15],  # curve 0 to 5, Zone 2
            [2.3, 0.50, 0.15],  # curve 0 to 5, Zone 3
        ],
        '15° to 35° chart': [
            [2.0, 0.56, 0.30],  # curve 15 to 35, Zone 1
            [2.9, 0.65, 0.40],  # curve 15 to 35, Zone 2
            [3.5, 0.80, 0.50],  # curve 15 to 35, Zone 3
        ],
    }

    return ParameterStandard(fig_29p4d7_dependent_axis, fig_29p4d7_indexes, fig_29p4d7_labels)
