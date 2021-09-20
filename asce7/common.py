from math import log10, pi, atan
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


class Log(float):
    """Representation for the log10 of a number."""

    def __new__(cls, value):
        return super(Log, cls).__new__(cls, log10(value))

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{type(self).__name__}({self.value})'

    def __format__(self, format_spec):
        return f'{type(self).__name__}({self.value:{format_spec}})'


class InfoArray(np.ndarray):
    """Same as numpy array but can have an info attribute"""

    def __new__(cls, input_array, info=None):
        # Input array is an array_like
        # We first cast to be our class type
        obj = np.asarray(input_array).view(cls)
        # add the new attribute to the created instance
        obj.info = info
        # Finally, we must return the newly created object:
        return obj

    def __array_finalize__(self, obj):
        # see InfoArray.__array_finalize__ for comments
        if obj is None:
            return
        self.info = getattr(obj, 'info', None)


def iter_keys_view_if_has_a_keys_view(*args):
    """Iterate over keys views if they exist."""

    yield from (keys() for input in args if (keys := getattr(input, "keys", None)) is not None)
