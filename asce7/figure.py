"""For implementing lookups in figures provided by the building code."""
from dataclasses import dataclass
from decimal import Decimal
from numbers import Real
from typing import Callable, TypeVar, Iterable, Sequence
from asce7.interpolate import piecewise_interpolator

T = TypeVar("T")
Number = TypeVar("Number", Real, Decimal, float)
NumberFunc = Callable[..., Number]


def _return_value(value: T) -> T:
    """Just return the value."""
    return value


class _VariableSeq(list):
    """The independent or dependent variables of a curve

    Provides the values that make the curve, and functions to convert the values to and from the axis value (which may
    or may not be the same as the curve value).
    """

    def __new__(cls, value, /, from_axis: NumberFunc = _return_value, from_curve: NumberFunc = _return_value):
        return super().__new__(cls, value)

    def __init__(self, value, /, from_axis: NumberFunc = _return_value, from_curve: NumberFunc = _return_value):
        super().__init__(value)
        self.from_axis = from_axis
        self.from_curve = from_curve


@dataclass(repr=False)
class Curve:
    """Piecewise curves making up a figure."""

    def __init__(self, independent: Iterable[Number] = None, dependent: Iterable[Number] = None):
        self.independent = _VariableSeq(independent if independent is not None else [])
        self.dependent = _VariableSeq(dependent if independent is not None else [])
        self.interpolate = piecewise_interpolator([self.independent.from_axis(i) for i in self.independent],
                                                  [self.dependent.from_axis(d) for d in self.dependent])

    def __repr__(self):
        return f"({self.independent!r}, {self.dependent!r})"

    def lookup(self, value: Number) -> Number:
        dependent_value = self.dependent.from_axis(value)
        independent_value = self.interpolate(dependent_value)
        return self.dependent.from_curve(independent_value)

    @property
    def from_dependent(self) -> NumberFunc:
        return self.dependent.from_curve

    @from_dependent.setter
    def from_dependent(self, func: NumberFunc):
        self.dependent.from_curve = func if func is not None else _return_value

    @property
    def to_dependent(self) -> NumberFunc:
        return self.dependent.from_axis

    @to_dependent.setter
    def to_dependent(self, func: NumberFunc):
        self.dependent.from_axis = func if func is not None else _return_value

    @property
    def from_independent(self) -> NumberFunc:
        return self.independent.from_curve

    @from_independent.setter
    def from_independent(self, func: NumberFunc):
        self.independent.from_curve = func if func is not None else _return_value

    @property
    def to_independent(self) -> NumberFunc:
        return self.independent.from_axis

    @to_independent.setter
    def to_independent(self, func: NumberFunc):
        self.independent.from_axis = func if func is not None else _return_value


class Figure:
    """An ASCE 7 building code figure."""

    def __init__(self, **curves: tuple[Sequence[Number], Sequence[Number]]):
        vars(self).update(**{k:Curve(*c) for k, c in curves.items()})

    def __repr__(self):
        return f"{type(self).__name__}({', '.join(f'{k}={v!r}' for k, v, in vars(self).items())})"
