"""CHAPTER 2
COMBINATIONS OF LOADS
"""

from ceng.load import Combination


class Strength:
    """cf. Section 2.3"""

    @Combination("1.4*D").method
    def dead_load(self, D=0):
        """Strength Load Combo 1"""
        ...

    @Combination("1.2*D & 1.6*L & 0.5*(Lr | S | R)").method
    def live_primary_load(self, D=0, L=0, Lr=0, S=0, R=0):
        """Strength Load Combo 2"""
        ...

    @Combination("1.2*D & 1.6*(S | Lr | R) & (1.0*L | 0.5*W)").method
    def roof_snow_rain_primary_load(self, D=0, S=0, Lr=0, R=0, L=0, W=0):
        """Strength Load Combo 3"""
        ...

    @Combination("1.2*D & W & L & 0.5*(Lr | S | R)").method
    def wind_primary_load(self, D=0, W=0, L=0, Lr=0, S=0, R=0):
        """Strength Load Combo 4"""
        ...

    @Combination("0.9*D & W").method
    def wind_up_load(self, D=0, W=0):
        """Strength Load Combo 5"""
        ...


class ASD:
    """cf. Section 2.4"""

    @Combination("D").method
    def dead_load(self, D=0):
        """ASD Load Combo 1"""
        ...

    @Combination("D & L").method
    def live_load(self, D=0, L=0):
        """ASD Load Combo 2"""
        ...

    @Combination("D & (S | Lr | R)").method
    def roof_snow_rain_load(self, D=0, S=0, Lr=0, R=0):
        """ASD Load Combo 3"""
        ...

    @Combination("D & 0.75*L & 0.75*(Lr | S | R)").method
    def live_primary_load(self, D=0, L=0, Lr=0, S=0, R=0):
        """ASD Load Combo 4"""
        ...

    @Combination("D & 0.6*W").method
    def wind_down_load(self, D=0, W=0):
        """ASD Load Combo 5"""
        ...

    @Combination("D & 0.75*L & 0.75*0.6*W & 0.75*(Lr | S | R)").method
    def wind_primary_load(self, D=0, L=0, W=0, Lr=0, S=0, R=0):
        """ASD Load Combo 6"""
        ...

    @Combination("0.6*D & 0.6*W").method
    def wind_up_load(self, D=0, W=0):
        """ASD Load Combo 7"""
        ...
