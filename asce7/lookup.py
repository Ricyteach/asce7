"""For implementing lookups in parameter standards (figures and tables) provided by the building code.

ASCE 7 often presents figures with multiple charts, or multiple tables, and each chart or table with multiple curves or
series. The charts or tables are in a sequence and intended to be interpolated between each other, and a second
interpolation happens along the curve or series."""


import dataclasses
import scipy.interpolate
import pandas as pd
from .types import Any, Sequence, Mapping, Number, Union

INTERP_ND_DICT = {1: scipy.interpolate.interp1d, 2: scipy.interpolate.interp2d}


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

    data: Union[Sequence[Sequence[Sequence[Number]]],
                Sequence[Sequence[Number]]]
    index: Mapping[Any, Sequence]
    labels: Mapping[Any, Sequence]
    df: pd.DataFrame = dataclasses.field(init=False, repr=False)
    lookup: pd.Series = dataclasses.field(init=False, repr=False)

    def __post_init__(self):
        number_of_independent_variables = len(self.index)
        data: Sequence[Sequence[Sequence[Number]]]
        if number_of_independent_variables == 1:
            data = [self.data]
        elif number_of_independent_variables == 2:
            data = self.data
        else:
            raise TypeError("only 1 or 2 indexes supported")

        label_name, = self.labels.keys()
        labels, = self.labels.values()

        z = (row for section in data for row in zip(*section))
        m = pd.MultiIndex.from_product(self.index.values(), names=self.index.keys())
        c = pd.Index(labels, name=label_name)
        df = self.df = pd.DataFrame(z, index=m, columns=c)

        interpNd = INTERP_ND_DICT[number_of_independent_variables]
        self.lookup = pd.Series([interpNd(*m.levels, df[k]) for k in df.columns], index=df.columns)
