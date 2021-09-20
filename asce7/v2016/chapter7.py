"""ASCE 7 Figures"""
from asce7.interp import interp_dict
from types import SimpleNamespace

_FIG7P4D1_Cs__STR = """
                        C_t
                        1.0     1.1     1.2
Surface Type    C_s
slippery        1.0     0       0       0
                1.0     5       10      15
                0       70      70      70
                0       90      90      90
other           1.0     0       0       0
                1.0     30      37.5    45
                0       70      70      70
                0       90      90      90
""".replace("    ", "\t")[1:-1]

FIG7P4D1_Cs_NS = SimpleNamespace()
# Z values
FIG7P4D1_Cs_NS.Cs = (1.0, 1.0, 0, 0)
# Y values
FIG7P4D1_Cs_NS.Ct = (1.0, 1.1, 1.2)
# X values
FIG7P4D1_Cs_NS.roof_slope = dict(
    slippery=[
        [0, 5, 70, 90],
        [0, 10, 70, 90],
        [0, 15, 70, 90],
    ],
    other=[
        [0, 30, 70, 90],
        [0, 37.5, 70, 90],
        [0, 45, 70, 90],
    ]
)

FIG7P4D1_Cs_NS_DICT = interp_dict(
    x=FIG7P4D1_Cs_NS.roof_slope,
    y=FIG7P4D1_Cs_NS.Ct,
    z=FIG7P4D1_Cs_NS.Cs,
    axis=0
)


def fig7p4d1_Cs(surface_type, roof_slope, temp_coefficient):
    """Figure 7.4-1: Roof slope factor, Cs, for warm and cold roofs

    (Table 7.3-2 for Ct definitions)
    """
    return FIG7P4D1_Cs_NS_DICT[surface_type](roof_slope, temp_coefficient)
