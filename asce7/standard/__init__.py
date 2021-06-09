"""Tools for implementation of design standards. Primarily intended for usage in conjunction with engineering design
codes."""

import dataclasses
import itertools
import types
from typing import Sequence, Union, Iterable, Sized, ClassVar, cast, TypedDict, Optional, Mapping

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d, interp2d

SizedIterable = types.new_class("SizedIterable", (Sized, Iterable), {})

try:
    del pd.DataFrame.lookup
except AttributeError:
    pass


class StrictDivisionError(ValueError):
    def __init__(self):
        super().__init__("modulo operation resulted in a remainder")


def all_equal(iterable):
    """Returns False if all the elements are not equal to each other, returns (value, grouper iterator) otherwise."""

    g = itertools.groupby(iterable)
    if (result := next(g, True)) and next(g, None) is None:
        return result
    return False


def strict_integer_division(numerator: int, denominator: int) -> int:
    """Integer division; no remainder is allowed."""

    result = bool(numerator % denominator) or numerator // denominator
    if result is True:
        raise StrictDivisionError()
    else:
        return result


def _shape_matched_dataframe(xyz_mapping: Mapping, *, index: Optional[pd.Index] = None) -> pd.DataFrame:
    n_rows = len(index) if index is not None else None

    arg_arrays = {k: np.array(v) for k, v in xyz_mapping.items()}
    arg_dimensions = {k: v.ndim for k, v in arg_arrays.items()}
    arg_shapes = {k: v.shape for k, v in arg_arrays.items()}

    max_dimensions = max(arg_dimensions.values())
    max_dim_keys = tuple(k for k, v in arg_dimensions.items() if v == max_dimensions)

    if max_dimensions > 2:
        raise TypeError(f"Invalid max. argument dimensions, {max_dim_keys!r}:{max_dimensions:d}")
    elif max_dimensions == 1 and n_rows is None:
        raise TypeError("Must provide number of rows if all arguments are 1d")
    elif max_dimensions == 2:
        n_rows_lst = [arg_arrays[k].shape[0] for k in max_dim_keys]
        if all_equal(n_rows_lst):
            n_rows_from_args = n_rows_lst[0]
        else:
            raise TypeError(f"The shapes of the 2d arrays {' and '.join(max_dim_keys)} do not match")
        if n_rows is None:
            n_rows = n_rows_from_args
        else:
            if n_rows != n_rows_from_args:
                raise TypeError(f"The provided number of rows and {', '.join(max_dim_keys)} 2d array shape(s) do not match")

    if arg_shapes["y"] == ():
        # 1d interpolation case
        for arg_name, arg in arg_arrays.items():
            if arg_dimensions[arg_name] == 1:
                arg_arrays[arg_name] = [arg] * n_rows
    else:
        # 2d interpolation case
        # min_dimensions = min(arg_dimensions.values())
        # min_dim_keys = tuple(k for k, v in arg_dimensions.items() if v == min_dimensions)
        # if min_dimensions < 1:
        #     raise TypeError(f"Invalid min. argument dimensions, {', '.join(min_dim_keys)}:{min_dimensions:d}")
        #
        if max_dimensions == 1:
            n_columns = arg_shapes["x"][0] * arg_shapes["y"][0]
        else:
            try:
                n_columns, _ = all_equal(v[1] for k, v in arg_shapes.items() if arg_dimensions[k] == 2)
            except TypeError:
                raise TypeError(f"The shapes of the 2d arrays {' and '.join(max_dim_keys)} do not match") from None

        for arg_name, arg in arg_arrays.items():
            if arg_dimensions[arg_name] == 1:
                arg_1d_shape = arg_shapes[arg_name][0]
                arg_arrays[arg_name] = np.tile(arg, (n_rows, strict_integer_division(n_columns, arg_1d_shape)))

    if not all_equal(v.shape for v in arg_arrays.values()):
        raise TypeError(f"The shapes of the arrays are incompatible")



    return pd.DataFrame(np.hstack(arg_arrays.values()), index=index)


@dataclasses.dataclass(repr=False)
class StandardLookup:
    """For interpolation lookups on tables, charts, and figures."""

    x: Union[Sequence[float], Sequence[Sequence[float]]]
    y: Union[Sequence[float], Sequence[Sequence[float]]]
    z: Union[Sequence[float], Sequence[Sequence[float]]]
    index: Iterable
    columns: ClassVar[SizedIterable]
    df: pd.DataFrame = dataclasses.field(init=False)

    def __post_init__(self):
        self.df = _shape_matched_dataframe(dict(x=self.x, y=self.y, z=self.z), index=self.index)
        self.df["lookup"] = lambda x, y: "spam"

    @property
    def index(self) -> pd.Index:
        return self._index

    @index.setter
    def index(self, value: Iterable):
        try:
            df = self.df
        except AttributeError:
            self._index = value if isinstance(value, pd.Index) else pd.Index(value)
        else:
            df.index = cast(pd.Index, value)
            self._index = df.index

    @property
    def columns(self) -> pd.Index:
        return self.df.columns

    @columns.setter
    def columns(self, value: SizedIterable):
        self.df.columns = value

    @property
    def lookup(self):
        return self.df.lookup

    def __repr__(self):
        return repr(self.df.drop('lookup', axis=1)).replace("DataFrame", type(self).__name__, 1)
