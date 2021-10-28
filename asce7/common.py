from functools import partial
from math import pi, atan
import numpy as np


class SlopeIn12(float):
    """Representation of an angle as change in height over 12 inches. Height is in inches."""

    def __new__(cls, value):
        return super(SlopeIn12, cls).__new__(cls, atan(value/12))

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{type(self).__name__}({self.value})'

    def __format__(self, format_spec):
        return f'{type(self).__name__}({self.value:{format_spec}})'


class Deg(float):
    """Representation of an angle in degrees."""

    def __new__(cls, value):
        return super(Deg, cls).__new__(cls, value * pi/180)

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{type(self).__name__}({self.value})'

    def __format__(self, format_spec):
        return f'{type(self).__name__}({self.value:{format_spec}})'


class Log(np.ndarray):
    """Representation for the log10 of a number."""

    def __new__(cls, value):
        obj = np.asarray(np.log10(value)).view(cls)
        obj.value = value
        return obj

    def __repr__(self):
        return f'{type(self).__name__}({self.value})'

    def __format__(self, format_spec):
        return f'{type(self).__name__}({self.value:{format_spec}})'

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.value = getattr(obj, 'value', None)


def attach_filter(filter_func, func=None):
    """Add a `filter` attribute to the function so it can be used elsewhere."""

    if func is None:
        return partial(attach_filter, filter_func)

    func.filter = filter_func
    return func
