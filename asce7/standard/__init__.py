"""Tools for implementation of design standards. Primarily intended for usage in conjunction with engineering design
codes."""

import dataclasses
import math
import types
from typing import Sequence, Union, Iterable, Sized, ClassVar, cast, TypedDict, Optional, Literal, TypeVar

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d, interp2d

from asce7.equal import all_equal

SizedIterable = types.new_class("SizedIterable", (Sized, Iterable), {})
FloatSeq_1D_or_2D = Union[Sequence[float], Sequence[Sequence[float]]]
T = TypeVar("T")
XYZ = Literal["x", "y", "z"]


class XYZDict(TypedDict, total=False):
    x: T
    y: T
    z: T


try:
    del pd.DataFrame.lookup
except AttributeError:
    pass


class StrictDivisionError(ValueError):
    def __init__(self):
        super().__init__("modulo operation resulted in a remainder")


def strict_integer_division(numerator: int, denominator: int) -> int:
    """Integer division; no remainder is allowed."""

    result = bool(numerator % denominator) or numerator // denominator
    if result is True:
        raise StrictDivisionError()
    else:
        return result


def _xyz_shapes_to_buckets(shapes: XYZDict, shapes_1d: XYZDict, shapes_2d: XYZDict) -> None:
    # split all the shapes into 1d and 2d buckets. y may be None (for 1d interpolation)
    name: XYZ
    for name, shape in shapes.items():
        if len(shape) not in (1,2):
            if not shape and name != "y":
                raise TypeError(f"{name:s} is atomic, must be a 1d or 2d sequence")
            elif not shape:
                continue
            raise TypeError(f"{name:s} has invalid shape, {shape!r}")

        try:
            shapes_1d[name], = shape
        except ValueError:
            shapes_2d[name] = _, _ = shape


def _get_xyz_n_rows(index: Optional[pd.Index], shapes_2d: XYZDict) -> int:
    n_rows: int = len(index) if index is not None else None

    if not shapes_2d:
        # for the case of all 1d arguments, an index has to be specified to count the rows
        if n_rows is None:
            raise TypeError("Must provide an index if all arguments are 1d")
    else:
        # in all cases with 2d arguments, number of rows is assumed to be shape_2d[0] (and all shape_2d[0] are equal)
        equal_rows = all_equal([shape_2d[0] for shape_2d in shapes_2d.values()])
        if equal_rows and n_rows is None:
            n_rows = equal_rows.value
        elif equal_rows and n_rows != equal_rows.value:
            raise TypeError(f"n_rows and number of rows in {', '.join(shapes_2d.keys())} 2d array(s)) do not match")
        elif not equal_rows:
            raise TypeError(f"Number of rows in the 2d arrays {' and '.join(shapes_2d.keys())} do not match") from None
        else:
            # the n_rows from the supplied index is fine, do nothing
            pass
    return n_rows


def _get_xyz_lengths(shapes_1d: XYZDict, shapes_2d: XYZDict) -> XYZDict:
    lengths = {}

    # argument lengths for 1d arguments x or y assumed to just be the shape_1d length (even if some arguments are 2d)
    lengths.update(**{name: v for name, v in shapes_1d.items() if name != "z"})

    # argument lengths for 2d arguments x or (optionally) y assumed to just be the z argument length divided by the
    # other shape_1d argument length if it exists. if both are 2d, or one is missing, assume it is the shape_2d[1]
    yx: XYZ
    switch_xy = {"x": "y", "y": "x"}
    for xy, xy_over_length in ((name, value) for name, (value, _) in shapes_2d.items() if name != "z"):
        yx = cast(XYZ, switch_xy[xy])
        try:
            yx_length = shapes_1d[yx]
        except KeyError:
            # both are 2d or one (hopefully y) is missing
            lengths[xy] = xy_over_length
        else:
            lengths[xy] = strict_integer_division(xy_over_length, yx_length)

    # SANITY CHECKS

    # in cases with all 2d arguments, all shape_2d[1] are equal
    equal_lengths = all_equal([shape_2d[1] for shape_2d in shapes_2d.values()])
    if not equal_lengths:
        raise TypeError(f"Argument lengths of {' and '.join(shapes_2d.keys())} do not match") from None
    lengths.update(**{name: equal_lengths.value for name in shapes_2d.keys()})

    if math.prod(length for name, length in lengths.items() if name != "z") != lengths["z"]:
        raise TypeError(f"The z length is not compatible with the {' and '.join(lengths.keys())} length(s)")

    return lengths


def _shape_matched_dataframe(xyz_dct: XYZDict, *, index: Optional[pd.Index] = None) -> pd.DataFrame:

    arguments = ("x", "y", "z")

    # PREPARATION OF NEEDED INFORMATION
    name: XYZ

    arrays: XYZDict = {name: np.array(xyz_dct[cast(XYZ, name)]) for name in arguments}
    shapes: XYZDict = {arg_name: v.shape for arg_name, v in arrays.items()}

    # split all the shapes into 1d and 2d buckets (y may be None for 1d interpolation)
    shapes_1d = cast(XYZDict, {})  # 1d bucket
    shapes_2d = cast(XYZDict, {})  # 2d bucket
    _xyz_shapes_to_buckets(shapes, shapes_1d, shapes_2d)

    # DETERMINE THE NUMBER OF ROWS OF THE RESULTANT DATAFRAME
    n_rows = _get_xyz_n_rows(index, shapes_2d)

    # in all cases, final_length of a all arguments is assumed to be the max length of the last provided dimension
    final_length = max(arguments, key=lambda n: shapes[cast(XYZ, n)][-1])

    # DETERMINE THE ARGUMENT LENGTHS (NEEDED TO CONSTRUCT THE RESULTANT DATAFRAME)
    lengths = _get_xyz_lengths(shapes_1d, shapes_2d)

    # UPDATE THE ARRAYS

    if shapes["y"] == ():
        # 1d interpolation case
        for name, arg in arrays.items():
            if dimensions[name] == 1:
                arrays[name] = [arg] * n_rows
        column_multiindexes = {
            arg_name:pd.MultiIndex.from_product([[arg_name], range(shapes["x"][0])], names=("Axis", "x"))
            for arg_name in "xz"
        }
    else:
        # 2d interpolation case
        # min_dimensions = min(arg_dimensions.values())
        # min_dim_keys = tuple(k for k, v in arg_dimensions.items() if v == min_dimensions)
        # if min_dimensions < 1:
        #     raise TypeError(f"Invalid min. argument dimensions, {', '.join(min_dim_keys)}:{min_dimensions:d}")
        #
        if max_dimensions == 1:
            n_columns = shapes["x"][0] * shapes["y"][0]
        else:
            try:
                n_columns, _ = all_equal(v[1] for name, v in shapes.items() if dimensions[name] == 2)
            except TypeError:
                raise TypeError(f"The shapes of the 2d arrays {' and '.join(max_dim_keys)} do not match") from None

        for name, arg in arrays.items():
            if dimensions[name] == 1:
                arrays[name] = np.tile(arg, (n_rows, strict_integer_division(n_columns, shapes_1d[name])))

    if not all_equal(v.shape for v in arrays.values()):
        raise TypeError(f"The shapes of the arrays are incompatible")

    # MULTIINDEXES FOR COLUMNS

    # 1d interpolation case
    column_multiindexes = {
        arg_name:pd.MultiIndex.from_product([[arg_name], range(shapes["x"][0])], names=("Axis", "x"))
        for arg_name in "xz"
    }

    # 2d interpolation case
    column_multiindexes = {
        arg_name: pd.MultiIndex.from_product(
            [
                [arg_name],
                range(lengths["x"][-1]),
                range(lengths["y"][-1])
            ],
            names=("Axis", "x", "y")
        )
        for arg_name in "xyz"
    }

    return pd.DataFrame(np.hstack(arrays.values()), index=index)


@dataclasses.dataclass(repr=False)
class StandardLookup:
    """For interpolation lookups on tables, charts, and figures."""

    x: FloatSeq_1D_or_2D
    y: FloatSeq_1D_or_2D
    z: FloatSeq_1D_or_2D
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
