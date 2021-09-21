from enum import Enum
import pandas as pd


class LoadType(str, Enum):
    """cf. Sections 1.2.2 and 2.2"""
    dead = "D"
    live = "L"
    snow = "S"
    wind = "W"
    seismic = "E"
    live_roof = "Lr"
    rain = "R"
    dead_ice = "Di"
    fluid = "F"
    flood = "Fa"
    temperature = "T"
    D = "D"
    L = "L"
    S = "S"
    W = "W"
    E = "E"
    Lr = "Lr"
    R = "R"
    Di = "Di"
    F = "F"
    Fa = "Fa"
    T = "T"


class Risk(str, Enum):
    """Risk Category of Buildings and Other Structures for Flood, Wind, Snow, Earthquake, and Ice Loads.

    cf. Table 1.5-1
    """
    I = "I"
    II = "II"
    III = "III"
    IV = "IV"


TABLE_1P5D2_Ix = pd.DataFrame({LoadType.snow: [0.80, 1.00, 1.10, 1.20],
                               LoadType.dead_ice: [0.80, 1.00, 1.15, 1.25],
                               LoadType.seismic: [1.00, 1.00, 1.25, 1.50]},
                              index=list(Risk))


def importance_factor(risk, load_type):
    """cf. Table 1.5-2 Importance Factors"""
    return TABLE_1P5D2_Ix[LoadType(load_type)][Risk(risk)]
