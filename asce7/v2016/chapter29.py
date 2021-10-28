from types import SimpleNamespace
from asce7.common import Log, Deg, attach_filter
from ceng.interp import interp_dict
import numpy as np

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
""".replace("    ", "\t")[1:-1]

FIG29P4D7_GCrn_nom_NS = SimpleNamespace()
FIG29P4D7_GCrn_nom_NS.zone = list("123")  # roof zone (strings!)
FIG29P4D7_GCrn_nom_NS.tilt = (0, 5, 15, 35)  # deg - interpolate, inclusive
FIG29P4D7_GCrn_nom_NS.area = tuple(Log(v) for v in (1, 500, 5000))  # psf - interpolate, log10
FIG29P4D7_GCrn_nom_NS.GCrn_nom = ([[1.5, 0.35, 0.10],
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
    x=FIG29P4D7_GCrn_nom_NS.tilt,
    y=FIG29P4D7_GCrn_nom_NS.area,
    z=dict(zip(FIG29P4D7_GCrn_nom_NS.zone, FIG29P4D7_GCrn_nom_NS.GCrn_nom)),
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


def fig29p4d7_GCrn_nom(zone, tilt, area):
    """Figure 29.4-7: Design Wind Loads (All Heights): Rooftop Solar Panels for Enclosed and Partially Enclosed
    Buildings, Roof θ≤7°

    Nominal Net Pressure Coefficients (GCrn)nom
    """
    return FIG29P4D7_GCrn_nom_DICT[zone](tilt, Log(area))


@attach_filter(filter29p4p3)
def eq29p4d5_p(qh, GCrn):
    """Equation 29.4-5: design wind pressure for rooftop solar panels for buildings of all heights with flat roofs or
    gable or hip roofs with slopes less than 7°.

    p = qh*GCrn (lbf/sq ft)
    """
    return qh * GCrn


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


def filter29p4p4(θ, roof_type, Lp, ω, h2):
    """Section 29.4.3: Rooftop Solar Panels for Buildings of All Heights with Flat Roofs or Gable or Hip Roofs with
    Slopes Less Than 7°.

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
