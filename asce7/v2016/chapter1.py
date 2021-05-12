from enum import Enum
import pandas as pd


class LoadType(Enum):
    dead = "D"
    live = "L"
    snow = "S"
    wind = "W"
    seismic = "E"
    D = "D"
    L = "L"
    S = "S"
    W = "W"
    E = "E"


class RiskCategory(Enum):
    """Risk Category of Buildings and Other Structures for Flood, Wind, Snow, Earthquake, and Ice Loads.

    cf. Table 1.5-1
    """
    I = "I"
    II = "II"
    III = "III"
    IV = "IV"


_Table_1_pt_5_dsh_2 = pd.DataFrame({LoadType.snow: [0.80, 1.00, 1.10, 1.20],
                             LoadType.seismic: [1.00, 1.00, 1.25, 1.50]},
                            index=list(RiskCategory))


def importance_factor(load_type):
    return lambda risk: _Table_1_pt_5_dsh_2[LoadType(load_type)][RiskCategory(risk)]
