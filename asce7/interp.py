from scipy.interpolate import interp1d
import numpy as np
from math import prod
import itertools as it

# Note: interp2d doesn't give the right results. no idea why, so have to write own interp2d


def interp2d(x, y, z, axis = 0, bounds_error = True, fill_value = None):
    """Interpolate between multiple curves.

    x, y and z are arrays of values used to approximate some function f: z = f(x, y) which returns a scalar value z.
    Returns a function that uses spline interpolation as many as 3 times to find the value of new points.

    Parameters
    ----------
    x,y : array_like of numbers
        the independent data of the curve; either both 1d, or one of x and y can be 2d
    z : array_like of numbers
        the dependent data of the curve; either 1d or if both x and y are 1d, then 2d
    axis: int (0 or 1)
        axis of 2d argument assumed to correspond to:
            - 'x' if y' or 'z' is 2d
            - 'y' if 'x' is 2d
    bounds_error : bool, optional
        if True, when interpolated values are requested outside the domain of the input data (x,y),
        a ValueError is raised. If False, then fill_value is used.
    fill_value : number, optional
        If provided, the value to use for points outside the interpolation domain. If omitted (None),
        values outside the  domain are extrapolated via nearest-neighbor extrapolation.

    Returns
    -------
    interpolator function
        a function that interpolates values

    Raises
    ------
    ValueError
        when a value error
    """

    x_arr, y_arr, z_arr = (np.array(arg) for arg in (x, y, z))

    args_sorted = sorted((arr.size, name, arr) for name,arr in zip("xyz", (x_arr, y_arr, z_arr)))
    if size:=prod(tup[0] for tup in args_sorted[:2]) != args_sorted[-1][-1].size:
        raise ValueError(f"Invalid length input for arguments (x,y,z): ({x_arr.size},{y_arr.size},{z_arr.size})")

    name_smallest, smallest = args_sorted[0][1:]


def _interp1d_with_2d_z_list(x_arr, y_arr, z_arr, x_axis, bounds_error, fill_value):

    y_axis = abs(x_axis - 1)
    axis_dict = {x_axis: x_arr, y_axis: y_arr}
    row_arr, col_arr = (axis_dict[i] for i in (0,1))
    if (row_arr.size, col_arr.size) != z_arr.shape:
        raise ValueError(f"Shape of z does not match sizes of x and y with x at axis {x_axis} of z")

