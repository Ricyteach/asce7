from math import log10
import numpy as np


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
