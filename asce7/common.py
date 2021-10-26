from math import log10, pi, atan


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
