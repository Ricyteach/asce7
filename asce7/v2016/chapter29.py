import numpy as np
from ..lookup import ParameterStandard


_FIG29P4D7_GCrn_nom__STR = """
        area (sq ft)
        1       500     5000

        tilt (°)
        0° to 5°                15° to 35°
        5                       15

Zone    GCrn_nom    
1       1.5     0.35    0.10    2.0     0.56    0.30
2       2.0     0.45    0.15    2.9     0.65    0.40
3       2.3     0.50    0.15    3.5     0.80    0.50
""".replace("    ", "\t")


def _fig_29p4d7_GCrn_nom():
    """Figure 29.4-7: Design Wind Loads (All Heights): Rooftop Solar Panels for Enclosed and Partially Enclosed
    Buildings, Roof θ≤7°

    Nominal Net Pressure Coefficients (Gcrn)nom
    """
    seq = [value.strip() for line in _FIG29P4D7_GCrn_nom__STR[1:-1].split("\n") for value in line.strip().split(" " * 4)]
    labels = {seq[5][0]: [row[0] for row in seq[6:]]}  # Zone
    indexes = {seq[2][0]: [int(v) for v in seq[4]],  # tilt (deg)
               seq[0][0]: eval(seq[1][0]),  # area sq ft
               }
    fig_29p4d7_dependent_axis = {
        seq[3][0]: [eval(row[1]) for row in seq[6:]],  # 0° to 5° chart
        seq[3][1]: [eval(row[2]) for row in seq[6:]],  # 15° to 35° chart
    }

    return ParameterStandard(fig_29p4d7_dependent_axis, indexes, labels,
                             lookup_input_adjuster=lambda *args: (args[0], np.log10(args[1])))
