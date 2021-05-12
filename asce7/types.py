"""Type hints used in package"""

from typing import Callable, TypeVar, Sequence, Mapping, Any, Union
from decimal import Decimal
from numbers import Real
import numpy.typing as npt

T = TypeVar("T")
Number = TypeVar("Number", Real, Decimal, float)
NumberFunc = Callable[..., Union[Number, npt.ArrayLike]]
NumberSeq = Union[Sequence[Number], npt.ArrayLike]
