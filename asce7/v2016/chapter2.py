from enum import Enum

import numpy as np
from asce7.v2016.chapter1 import LoadType


class LoadComboClass():
    """cf. Section 2.1"""
    ...


class Strength(LoadComboClass):
    """cf. Section 2.3"""

    def dead_load(self, D):
        """Strength Load Combo 1"""
        return 1.4*D

    def live_primary_load(self, D, L, Lr=0, S=0, R=0):
        """Strength Load Combo 2"""
        return 1.2*D + 1.6*L + 0.5*np.maximum(Lr, S, R)

    def snow_primary_load(self, D, S, L=0, W=0):
        """Strength Load Combo 3 - snow primary"""
        return 1.2 * D + 1.6 * S + np.maximum(L, 0.5 * W)

    def live_roof_primary_load(self, D, Lr, L=0, W=0):
        """Strength Load Combo 3 - live roof primary"""
        return 1.2 * D + 1.6 * Lr + np.maximum(L, 0.5 * W)

    def rain_primary_load(self, D, R, L=0, W=0):
        """Strength Load Combo 3 - rain primary"""
        return 1.2 * D + 1.6 * R + np.maximum(L, 0.5 * W)

    def wind_primary_load(self, D, W, L=0, Lr=0, S=0, R=0):
        """Strength Load Combo 4"""
        return 1.2*D + W + L + 0.5*np.maximum(Lr, S, R)

    def wind_up_load(self, D, W):
        """Strength Load Combo 5"""
        return 0.9*D + W


class ASD(LoadComboClass):
    """cf. Section 2.4"""

    def dead_load(self, D):
        """ASD Load Combo 1"""
        return D

    def live_load(self, D, L):
        """ASD Load Combo 2"""
        return D + L

    def snow_load(self, D, S):
        """ASD Load Combo 3 - snow primary"""
        return D + S

    def live_roof_load(self, D, Lr):
        """ASD Load Combo 3 - live roof primary"""
        return D + Lr

    def rain_load(self, D, R):
        """ASD Load Combo 3 - rain primary"""
        return D + R

    def live_primary_load(self, D, L, Lr=0, S=0, R=0):
        """ASD Load Combo 4 - live primary"""
        return D + 0.75*L + 0.75*np.maximum(Lr, S, R)

    def wind_down_load(self, D, W, L=0, Lr=0, S=0, R=0):
        """ASD Load Combo 4"""
        return D + 0.6*W + L + 0.5*np.maximum(Lr, S, R)

    def wind_primary_load(self, D, L, W, Lr=0, S=0, R=0):
        """ASD Load Combo 6"""
        D + 0.75*L + 0.75* (0.6*W) + 0.75*np.maximum(Lr, S, R)

    def wind_up_load(self, D, W):
        """ASD Load Combo 7"""
        return 0.6*D + 0.6*W
