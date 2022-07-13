"""CHAPTER 30
WIND LOADS: COMPONENTS AND CLADDING
"""

from types import SimpleNamespace
from asce7.common import Deg, Log

#############################################################
# 30.3.2 Design Wind Pressures
#############################################################


def eq30p3d1_GCp_interpolant(figure):
    return EQ30P3D1_FIGURES_GCp_LOOKUP[figure]


# Fig. 30.3-1 Components and Cladding [h ≤ 60 ft (h ≤ 18.3 m)]: External Pressure Coefficients, (GCp ),
# for Enclosed and Partially Enclosed Buildings—Walls

# TODO

# Figs. 30.3-2A–I (flat roofs, gable roofs and hip roofs)

# Fig. 30.3-2A Components and Cladding [h ≤ 60 ft (h ≤ 18.3 m)]: External Pressure Coefficients, (GCp), for Enclosed
# and Partially Enclosed Buildings—Gable Roofs, θ ≤ 7°
_FIG30P3D2A_GCp_ROOF_STR = """
0 deg to 7 deg Roof Slope

Zone 1' 1 2 3 Down
area (sq ft)    1       10      100     2000
GCp             0.3     0.3     0.2     0.2

Zone 1' Up
area (sq ft)    1       100     1000    2000
GCp             -0.9    -0.9    -0.4    -0.4

Zone 1 Up
area (sq ft)    1       10      500     2000
GCp             -1.7    -1.7    -1.0    -1.0

Zone 2 Up
area (sq ft)    1       10      500     2000
GCp             -2.1    -2.1    -1.4    -1.4

Zone 3 Up
area (sq ft)    1       10      500     2000
GCp             -3.2    -3.2    -1.4    -1.4
"""[
    1:-1
]

FIG30P3D2A_GCp_ROOF_NS = SimpleNamespace()
FIG30P3D2A_GCp_ROOF_NS.roof_type = "gable"
FIG30P3D2A_GCp_ROOF_NS.roof_slope = (Deg(0), Deg(7))
FIG30P3D2A_GCp_ROOF_NS.location = ("roof", "overhang")
FIG30P3D2A_GCp_ROOF_NS.zone = ("1'", "1", "2", "3")
FIG30P3D2A_GCp_ROOF_DICT = {
    # TODO
}

FIG30P3D2A_GCp_DICT = {
    "roof": FIG30P3D2A_GCp_ROOF_DICT,
    # TODO: overhang figure
}


def filter29p4p4(h):
    """Section 30.3.2 Design Wind Pressures

    h (ft)
    """
    return h <= 60


def fig30p3d2A_GCp(location, zone, A):
    """For Equation 30.3-1: Design wind pressures on C&C elements of low-rise buildings and buildings with h ≤ 60 ft

    From Figure 30.3-2A: Components and Cladding [h ≤ 60 ft (h ≤ 18.3 m)]: External Pressure Coefficients, (GCp),
    for Enclosed and Partially Enclosed Buildings—Gable Roofs, θ ≤ 7°
    """
    return FIG30P3D2A_GCp_DICT[location][zone](Log(A))


def fig30p3d2A_zone_check(d1, d2, h):
    """From Figure 30.3-2A: zone definition figure for Zone 1', 1, 2, 3

    d1, d2: distances (ft) from two nearest building edges
    h: building height (ft) to eaves
    """
    ...  # TODO


# Fig. 30.3-3 (stepped roofs)

# TODO


# Fig. 30.3-4 (multispan gable roofs)

# TODO


# Figs. 30.3-5A–B (monoslope roofs)

# TODO


# Fig. 30.3-6 (sawtooth roofs)

# TODO


# Fig. 30.3-7 (domed roofs)

# TODO


# Fig. 27.3-3, Note 4 (arched roofs)

# TODO


# Fig. 27.3-3, Note 4 (arched roofs)

# TODO

# LOOKUP FOR ALL CHAPTER 30 GCp FIGURES

# TODO
EQ30P3D1_FIGURES_GCp_LOOKUP = dict(
    zip(
        (
            "walls",
            "flat",
            "gable",
            "hip",
            "stepped",
            "multispan gable",
            "monoslope",
            "sawtooth",
            "domed",
            "arched",
        ),
        (NotImplemented,) * 2 + (fig30p3d2A_GCp,) * 3 + (NotImplemented,) * 5,
    )
)
