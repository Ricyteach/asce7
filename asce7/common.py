from math import log10


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
