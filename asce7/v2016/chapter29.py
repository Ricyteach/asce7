import numpy as np
from ..lookup import ParameterStandard

# Figure 29.4-7: Gcrn(nom)
FIG_29p4d7_LABELS = {'Zone': [1, 2, 3]}
FIG_29p4d7_INDEXES = {
                        'tilt (°)': (5, 15),  # degrees
                        'log area (sq ft)': np.log10([1, 500, 5000]),  # log sq ft
                      }
FIG_29p4d7_DEPENDENT_AXIS = dict(
    chart_0to5 = [
        [1.5, 0.35, 0.10],  # curve 0 to 5, Zone 1
        [2.0, 0.45, 0.15],  # curve 0 to 5, Zone 2
        [2.3, 0.50, 0.15],  # curve 0 to 5, Zone 3
    ],
    chart_10to15=[
        [2.0, 0.56, 0.30],  # curve 15 to 35, Zone 1
        [2.9, 0.65, 0.40],  # curve 15 to 35, Zone 2
        [3.5, 0.80, 0.50],  # curve 15 to 35, Zone 3
    ],
)

_FIG_29p4d7_STANDARD = ParameterStandard(list(FIG_29p4d7_DEPENDENT_AXIS.values()),
                                         FIG_29p4d7_INDEXES, FIG_29p4d7_LABELS)
