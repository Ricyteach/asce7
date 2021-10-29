"""CHAPTER 29
WIND LOADS ON BUILDING APPURTENANCES AND OTHER STRUCTURES:
MAIN WIND FORCE RESISTING SYSTEM (DIRECTIONAL PROCEDURE)

• Basic wind speed, V (Section 26.5);
• Wind directionality factor, Kd (Section 26.6);
• Exposure category (Section 26.7);
• Topographic factor, Kzt (Section 26.8);
• Ground elevation factor, Ke (Section 26.9); and
• Enclosure classification (Section 26.12).
"""

from types import SimpleNamespace
from asce7.common import Log, Deg, attach_filter
from ceng.interp import interp_dict, interp1d
import numpy as np

##########################################################
# 29.4.3 Rooftop Solar Panels for Buildings of All Heights
# with Flat Roofs or Gable or Hip Roofs with Slopes
# Less Than 7°
###########################################################

# Fig. 29.4-7 Design Wind Loads (All Heights): Rooftop Solar Panels for Enclosed and Partially Enclosed Buildings,
# Roof θ≤7°
_FIG29P4D7_GCrn_nom__STR = """
        area (sq ft)
        1       500     5000

        tilt (°)
        0° to 5°                                        15° to 35°
        0                       5                       15                      35

Zone    GCrn_nom    
1       1.5     0.35    0.10    1.5     0.35    0.10    2.0     0.56    0.30    2.0     0.56    0.30
2       2.0     0.45    0.15    2.0     0.45    0.15    2.9     0.65    0.40    2.9     0.65    0.40
3       2.3     0.50    0.15    2.3     0.50    0.15    3.5     0.80    0.50    3.5     0.80    0.50
"""[1:-1]

FIG29P4D7_γa_NS = SimpleNamespace()
FIG29P4D7_γa_NS.zone = list("123")  # roof zone (strings!)
FIG29P4D7_γa_NS.tilt = (0, 5, 15, 35)  # deg - interpolate, inclusive
FIG29P4D7_γa_NS.area = tuple(Log(v) for v in (1, 500, 5000))  # psf - interpolate, log10
FIG29P4D7_γa_NS.GCrn_nom = ([[1.5, 0.35, 0.10],
                             [1.5, 0.35, 0.10],
                             [2.0, 0.56, 0.30],
                             [2.0, 0.56, 0.30], ],
                            [[2.0, 0.45, 0.15],
                             [2.0, 0.45, 0.15],
                             [2.9, 0.65, 0.40],
                             [2.9, 0.65, 0.40], ],
                            [[2.3, 0.50, 0.15],
                             [2.3, 0.50, 0.15],
                             [3.5, 0.80, 0.50],
                             [3.5, 0.80, 0.50], ],
                            )

FIG29P4D7_GCrn_nom_DICT = interp_dict(
    x=FIG29P4D7_γa_NS.tilt,
    y=FIG29P4D7_γa_NS.area,
    z=dict(zip(FIG29P4D7_γa_NS.zone, FIG29P4D7_γa_NS.GCrn_nom)),
    axis=0
)


def filter29p4p3(θ, roof_type, Lp, ω, h1, h2):
    """Section 29.4.3: Rooftop Solar Panels for Buildings of All Heights with Flat Roofs or Gable or Hip Roofs with
    Slopes Less Than 7°.

    slope (deg)
    roof_type
    Lp (ft)
    ω (deg)
    h1 (ft)
    h2 (ft)
    """
    return (θ <= Deg(7)) & \
           np.in1d(roof_type, ["flat", "gable", "hip"]) & \
           (Lp <= 6.7) & \
           (ω <= Deg(35)) & \
           (h1 <= 2) & \
           (h2 <= 4)


@attach_filter(filter29p4p3)
def eq29p4d5_p(qh, GCrn):
    """Equation 29.4-5: design wind pressure for rooftop solar panels for buildings of all heights with flat roofs or
    gable or hip roofs with slopes less than 7°.

    p = qh*GCrn (lbf/sq ft)
    """
    return qh * GCrn


@attach_filter(filter29p4p3)
def eq29p4d6_GCrn_nom(zone, tilt, area):
    """For Equation 29.4-6: Nominal Net Pressure Coefficient, (GCrn)nom

    From Figure 29.4-7: Design Wind Loads (All Heights): Rooftop Solar Panels for Enclosed and Partially Enclosed
    Buildings, Roof θ≤7°
    """
    return FIG29P4D7_GCrn_nom_DICT[zone](tilt, Log(area))


@attach_filter(filter29p4p3)
def eq29p4d6_GCrn(γp, γc, γE, GCrn_nom):
    """Equation 29.4-6:

    GCrn = γp*γc*γE*GCrn_nom
    """
    return γp * γc * γE * GCrn_nom


@attach_filter(filter29p4p3)
def eq29p4d6_γp(hpt, h):
    """Equation 29.4-6 parapet height factor, γp:

    γp = min(1.2, 0.9 + hpt∕h)
    """
    return np.minimum(1.2, 0.9 + hpt/h)


@attach_filter(filter29p4p3)
def eq29p4d6_γc(Lp):
    """Equation 29.4-6 chord length factor, γc:

    γc = max(0.6 + 0.06*Lp, 0.8)
    """
    return np.maximum(0.6 + 0.06*Lp, 0.8)


EQ29P4D6_γE = {"exposed": 1.5, "unexposed": 1.0}


@attach_filter(filter29p4p3)
def eq29p4d6_γE(exposure_condition):
    """Equation 29.4-6 edge factor, γE:

    γE = 1.5 if exposed, 1.0 for any other condition
    """
    return EQ29P4D6_γE[exposure_condition]


#############################################################
# 29.4.4 Rooftop Solar Panels Parallel to the Roof Surface on
# Buildings of All Heights and Roof Slopes
#############################################################
def filter29p4p4(θ, roof_type, Lp, ω, h2):
    """Section 29.4.4 Rooftop Solar Panels Parallel to the Roof Surface on Buildings of All Heights and Roof Slopes.

    slope (deg)
    roof_type
    Lp (ft)
    ω (deg)
    h2 (ft)
    """
    return (θ <= Deg(7)) & \
           np.in1d(roof_type, ["flat", "gable", "hip"]) & \
           (Lp <= 6.7) & \
           (ω <= Deg(2)) & \
           (h2 <= 10 / 12)


@attach_filter(filter29p4p4)
def eq29p4d7_p(qh, GCp, γE, γa):
    """Equation 29.4-7:

    p= qh*GCp*γE*γa (lb ∕ft2)
    """
    return qh * GCp * γE * γa


EQ29P4D7_γE = {"exposed": 1.5, "unexposed": 1.0}


@attach_filter(filter29p4p4)
def eq29p4d7_γE(exposure_condition):
    """Equation 29.4-7 edge factor, γE:

    γE = 1.5 if exposed, 1.0 for any other condition
    """
    return EQ29P4D7_γE[exposure_condition]


# Fig. 29.4-8 Solar Panel Pressure Equalization Factor, γa, for Enclosed and Partially Enclosed Buildings
# of All Heights
_FIG29P4D8_γa__STR = """
Effective Wind Area, A (ft2)    γa    
1                               0.8
10                              0.8
100                             0.4
1000                            0.4
"""[1:-1]

FIG29P4D8_γa_NS = SimpleNamespace()
# X values
FIG29P4D8_γa_NS.A = tuple(Log(v) for v in [1, 10, 100, 1000])  # effective wind area (ft2)
# Y values
FIG29P4D8_γa_NS.γa = (0.8, 0.8, 0.4, 0.4)  # solar panel pressure equalization factor

FIG29P4D8_γa_INTERPOLANT = interp1d(FIG29P4D8_γa_NS.A, FIG29P4D8_γa_NS.γa)


@attach_filter(filter29p4p4)
def eq29p4d7_γa(A):
    """For Equation 29.4-7: solar panel pressure equalization factor, γa

    From Figure 29.4-8: Solar Panel Pressure Equalization Factor, γa, for Enclosed and Partially Enclosed Buildings
    of All Heights
    """
    return FIG29P4D8_γa_INTERPOLANT(Log(A))
