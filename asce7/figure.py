from dataclasses import dataclass
from decimal import Decimal
from numbers import Real
from typing import Callable, TypeVar, Iterable, Sequence
from asce7.interpolate import piecewise_interpolator

T = TypeVar("T")
Number = TypeVar("Number", Real, Decimal, float)
NumberFunc = Callable[..., Number]


def return_value(value: T) -> T:
    """Just return the value."""
    return value


class VariableSeq(list):
    """The independent or dependent variables of a curve

    Provides the values that make the curve, and functions to convert the values to and from the axis value (which may
    not be the same as the curve value).
    """

    def __new__(cls, value, /, from_axis: NumberFunc = return_value, from_curve: NumberFunc = return_value):
        return super().__new__(cls, value)

    def __init__(self, value, /, from_axis: NumberFunc = return_value, from_curve: NumberFunc = return_value):
        super().__init__(value)
        self.from_axis = from_axis
        self.from_curve = from_curve


@dataclass(repr=False)
class Curve:

    def __init__(self, independent: Iterable[Number] = None, dependent: Iterable[Number] = None):
        self.independent = VariableSeq(independent if independent is not None else [])
        self.dependent = VariableSeq(dependent if independent is not None else [])
        self.interpolate = piecewise_interpolator([self.independent.from_axis(i) for i in self.independent],
                                                  [self.dependent.from_axis(d) for d in self.dependent])

    def __repr__(self):
        return f"({self.independent!r}, {self.dependent!r})"

    def lookup(self, value: Number) -> Number:
        dependent_value = self.dependent.from_axis(value)
        independent_value = self.interpolate(dependent_value)
        return self.dependent.from_curve(independent_value)


class Figure:

    def __init__(self, **curves: tuple[Sequence[Real], Sequence[Real]]):
        vars(self).update(**{k:Curve(*c) for k,c in curves.items()})

    def __repr__(self):
        return f"{type(self).__name__}({', '.join(f'{k}={v!r}' for k, v, in vars(self).items())})"
