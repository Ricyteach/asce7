"""Implementation of the ASCE 7 2016 building code."""
from functools import partial

from .chapter1 import importance_factor, Risk, LoadType
# from . import chapter2 as load_combinations
# from . import chapter7 as snow
# from . import chapter11 as seismic
# from . import chapter12 as seismic_building
# from . import chapter13 as seismic_nonstructural_component
# from . import chapter15 as seismic_nonbuilding_structure
# from . import chapter26 as wind
# from . import chapter27 as wind_building_directional
# from . import chapter28 as wind_building_envelope
# from . import chapter29 as wind_other_structures
# from . import chapter30 as wind_components_and_cladding

__version__ = "0.1"

I_s = partial(importance_factor, load_type="S")
I_e = partial(importance_factor, load_type="E")
