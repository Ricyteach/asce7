"""For implementing lookups in parameter standards (figures and tables) provided by the building code.

ASCE 7 often presents figures with multiple charts, or multiple tables, and each chart or table with multiple curves or
series. The charts or tables are in a sequence and intended to be interpolated between each other, and a second
interpolation happens along the curve or series."""

import dataclasses
import functools
import scipy.interpolate
import pandas as pd
from .types import Any, Sequence, Mapping, NumberSeq, Callable

INTERP_ND_DICT = {1: scipy.interpolate.interp1d, 2: scipy.interpolate.interp2d}


def pass_through_args(*args):
    return args


def pass_through_obj(obj):
    return obj


@dataclasses.dataclass
class ParameterStandard:
    """Representation of the definition of a parameter used in calculations.

    data = [   # z, or dependent variable, interpolation values
                [   # chart or table a - interpolation value = 100
                    [1, 2, 3],  # sequence (table column or figure curve) 1 part a
                    [4, 5, 6],  # sequence (table column or figure curve) 2 part a
                ],
                [   # chart or table b - interpolation value = 1000
                    [10, 20, 30],  # sequence (table column or figure curve) 1 part b
                    [40, 50, 60],  # sequence (table column or figure curve) 2 part b
                ],
            ]
    labels = ['sequence 1', 'sequence 2']
    index = {
                'part a or b name': (100, 1000),  # x, or chart, interpolation values (a or b)
                'dependent name': (3, 7, 11),  # y, or independent variable, interpolation values
            }
    """

    data: Mapping[Any, Sequence[NumberSeq]]
    index: Mapping[Any, NumberSeq]
    labels: Mapping[Any, Sequence]
    df: pd.DataFrame = dataclasses.field(init=False, repr=False)
    lookup: pd.Series = dataclasses.field(init=False, repr=False)

    # adjusters
    lookup_input_adjuster: Callable = dataclasses.field(default=pass_through_args, repr=False)
    lookup_output_adjuster: Callable = dataclasses.field(default=pass_through_obj, repr=False)

    def __post_init__(self):
        self._set_df()
        self._set_lookup()

    def _set_df(self):
        label_name, = self.labels.keys()
        labels, = self.labels.values()

        z = list(row for section in self.data.values() for row in zip(*section))
        m = pd.MultiIndex.from_product(self.index.values(), names=self.index.keys())
        c = pd.Index(labels, name=label_name)
        self.df = pd.DataFrame(z, index=m, columns=c)

    def _set_lookup(self):
        number_of_independent_variables = len(self.index)
        if number_of_independent_variables not in (1,2):
            raise TypeError("only 1 or 2 indexes supported")

        df = self.df
        interpNd = INTERP_ND_DICT[number_of_independent_variables]

        @functools.wraps(interpNd)
        def index_interpolation_function_factory(*args):
            scipy_interpolation_function = interpNd(*args)

            @functools.wraps(scipy_interpolation_function)
            def wrapped_interpolation_function(*args):
                adjusted_args = self.lookup_input_adjuster(*args)
                unadjusted_result = scipy_interpolation_function(*adjusted_args)
                return self.lookup_output_adjuster(unadjusted_result)
            return wrapped_interpolation_function

        self.lookup = pd.Series([index_interpolation_function_factory(*df.index.levels, df[k])
                                 for k in df.columns], index=df.columns)
