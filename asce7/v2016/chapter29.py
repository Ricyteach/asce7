from types import SimpleNamespace
from asce7.common import Log
from asce7.interp import interp_dict


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
                                   [2.0, 0.56, 0.30],],
                                  [[2.0, 0.45, 0.15],
                                   [2.0, 0.45, 0.15],
                                   [2.9, 0.65, 0.40],
                                   [2.9, 0.65, 0.40],],
                                  [[2.3, 0.50, 0.15],
                                   [2.3, 0.50, 0.15],
                                   [3.5, 0.80, 0.50],
                                   [3.5, 0.80, 0.50],],
                                  )

FIG29P4D7_GCrn_nom_DICT = interp_dict(
    x=FIG29P4D7_GCrn_nom_NS.tilt,
    y=FIG29P4D7_GCrn_nom_NS.area,
    z=dict(zip(FIG29P4D7_GCrn_nom_NS.zone, FIG29P4D7_GCrn_nom_NS.GCrn_nom)),
    axis=0
)


def fig29p4d7_GCrn_nom(zone, tilt, area):
    """Figure 29.4-7: Design Wind Loads (All Heights): Rooftop Solar Panels for Enclosed and Partially Enclosed
    Buildings, Roof θ≤7°

    Nominal Net Pressure Coefficients (Gcrn)nom
    """
    return FIG29P4D7_GCrn_nom_DICT[zone](tilt, Log(area))
