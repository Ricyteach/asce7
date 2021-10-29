"""CHAPTER 26
WIND LOADS: GENERAL REQUIREMENTS
"""

import numpy as np

#############################################################
# 26.10 Velocity Pressure
#############################################################

# 26.10.1 Velocity Pressure Coefficient Kz

TABLE26P11D1_TERRAIN_EXPOSURE_CONSTANTS_STR = """
# TODO
"""[1:-1]


# 26.10.2 Velocity Pressure qz

def eq26p10d1_qz(Kz, Kzt, Kd, Ke, V):
    """Velocity pressure, qz, evaluated at height z above ground

    qz = 0.00256*Kz*Kzt*Kd*Ke*V**2 (lb∕ft2)
    """
    return 0.00256*Kz*Kzt*Kd*Ke*V**2


def eq26p10d1_Ke(zg):
    """Ground Elevation Factor, Ke, evaluated at elevation zg (ft) above sea level

    Ke = e**(-0.0000362*zg)

    From Table 26.9-1: Ground Elevation Factor, Ke
    """
    return np.exp(-0.0000362*zg)


def eq26p10d1_Kz(z):
    """
    For 15 ft ≤ z ≤ zg:
    Kz =2.01*(z∕zg)**(2∕α)
    For z < 15 ft:
    Kz =2.01(15∕zg)**(2∕α)
    """
    ...  # TODO
