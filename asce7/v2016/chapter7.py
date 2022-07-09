"""CHAPTER 7
SNOW LOADS
"""

import numpy as np
from asce7.common import Deg
from ceng.interp import interp_dict
from types import SimpleNamespace

#########################################
# flat roof snow load, pf
#########################################

# ---------------------------------------
#    Ce
# ---------------------------------------

_FIG7P3D1_STR = """
                                            Ce

                                            Snow Exposure
                                            Fully   Partially   Sheltered
Wind Surface Roughness
B                                           0.9     1.0         1.2
C                                           0.9     1.0         1.1
D                                           0.8     0.9         1.0
Windswept mountainous above tree line       0.7     0.8         nan
Alaska no trees within 2 mi radius          0.7     0.8         nan
"""[1:-1]


TABLE7P3D1_NS = SimpleNamespace()
TABLE7P3D1_NS.wind_surface_roughness = ("B", "C", "D", "Windswept mountainous above tree line",
                                           "Alaska no trees within 2 mi radius")
TABLE7P3D1_NS.snow_exposure = ("fully", "partially", "sheltered")
TABLE7P3D1_NS.Ce = {
    "B": [0.9, 1.0, 1.2],
    "C": [0.9, 1.0, 1.1],
    "D": [0.8, 0.9, 1.0],
    "Windswept mountainous above tree line": [0.7, 0.8, np.nan],
    "Alaska no trees within 2 mi radius": [0.7, 0.8, np.nan],
}
TABLE7P3D1_DICT = dict(zip(TABLE7P3D1_NS.wind_surface_roughness,
                              (dict(zip(TABLE7P3D1_NS.snow_exposure, seq)) for seq in TABLE7P3D1_NS.Ce.values())))


def Ce(wind_surface_roughness, snow_exposure):
    """Figure 7.3-1 Exposure factor, Ce

    (Table 7.3-1 for Ce definitions)
    """
    return TABLE7P3D1_DICT[wind_surface_roughness][snow_exposure]

# ----------------------------------
#   End Ce
# ----------------------------------


_TABLE7P3D2_Ct__STR = """
                                                                                    Ct
Thermal Condition
All structures except for those indicated below                                     1.0
Structures kept just above freezing with cold, ventilated roofs and min R-value 25  1.1
Unheated and open air structures                                                    1.2
Freezer building                                                                    1.3
Continuously heated greenhouses with max R-value of 2                               0.85
"""[1:-1]

TABLE7P3D2_Ct_NS = SimpleNamespace()
TABLE7P3D2_Ct_NS.thermal_condition = (
    "All structures except for those indicated below",
    "Structures kept just above freezing with cold, ventilated roofs and min R-value 25",
    "Unheated and open air structures",
    "Freezer building",
    "Continuously heated greenhouses with max R-value of 2",
)
TABLE7P3D2_Ct_NS.Ct = (1.0, 1.1, 1.2, 1.3, 0.85)
TABLE7P3D2_Ct_DICT = dict(zip(TABLE7P3D2_Ct_NS.thermal_condition, TABLE7P3D2_Ct_NS.Ct))


def table7p3d2_Ct(thermal_condition):
    """Figure 7.3-2 Thermal factor, Ct

    (Table 7.3-2 for Ct definitions)
    """
    return TABLE7P3D2_Ct_DICT[thermal_condition]


def eq7p3d1_pf(Ce, Ct, Is, pg):
    """Equation 7.4-1 flat roof snow load, pf:

    pf = Ce*Ct*Is*pg
    """
    return Ce*Ct*Is*pg


#########################################
# low-slope roof minimum snow load, pm
#########################################
_EQ7P3P4D1_15d = Deg(15)
_EQ7P3P4D1_10d = Deg(10)


def eq7p3p4d1_pm(roof_type, roof_slope, Is, pg):
    """Equation 7.3.4-1 minimum low-slope roof snow load, pm:

    if curved roof_slope < 10 deg or monoslope, hip, gable roof_slope < 15 deg:
    pm = Is*pg
    otherwise:
    pm = 0 (doesn't apply)

    NOTE: all roof_type entries other than "curved" are assumed to be monoslope, hip, or gable.
    """
    is_curved = roof_type == "curved"
    curved_w_slope_le_10d = is_curved & (roof_slope <= _EQ7P3P4D1_10d)
    non_curved_w_slope_le_15d = (1 ^ is_curved) & (roof_slope <= _EQ7P3P4D1_15d)
    return Is * np.minimum(pg, 20) * (non_curved_w_slope_le_15d | curved_w_slope_le_10d)


#########################################
# sloped roof snow load, ps
#########################################
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
"""[1:-1]

FIG7P4D1_Cs_NS = SimpleNamespace()
# Z values
FIG7P4D1_Cs_NS.Cs = (1.0, 1.0, 0, 0)
# Y values
FIG7P4D1_Cs_NS.Ct = (1.0, 1.1, 1.2)
# X values
FIG7P4D1_Cs_NS.roof_slope = dict(
    slippery=[
        [Deg(v) for v in [0, 5, 70, 90]],
        [Deg(v) for v in [0, 10, 70, 90]],
        [Deg(v) for v in [0, 15, 70, 90]],
    ],
    other=[
        [Deg(v) for v in [0, 30, 70, 90]],
        [Deg(v) for v in [0, 37.5, 70, 90]],
        [Deg(v) for v in [0, 45, 70, 90]],
    ]
)

FIG7P4D1_Cs_DICT = interp_dict(
    x=FIG7P4D1_Cs_NS.roof_slope,
    y=FIG7P4D1_Cs_NS.Ct,
    z=FIG7P4D1_Cs_NS.Cs,
    axis=0
)


def fig7p4d1_Cs(surface_type, roof_slope, temp_coefficient):
    """Figure 7.4-1: Roof slope factor, Cs, for warm and cold roofs

    (Table 7.3-2 for Ct definitions)
    """
    return FIG7P4D1_Cs_DICT[surface_type](roof_slope, temp_coefficient)


def eq7p4d1_ps(Cs, pf):
    """Equation 7.4-1 sloped roof snow load, ps:

    ps = Cs*pf
    """
    return Cs*pf


#########################################
# rain on snow surcharge load, R
#########################################
def eq7p10d1_R(pg, roof_slope, W):
    """Equation 7.10-1 rain on snow surcharge load, R:

    if pg>0 and pg<=20 (psf) and roof_slope (deg) < W/50 (ft):
    R = 5 (psf)
    otherwise:
    R = 0
    """
    pg_le_20psf_and_nonzero = (pg <= 20) & (pg > 0)
    low_slope = roof_slope < (W/50)
    return 5 * (pg_le_20psf_and_nonzero | low_slope)
