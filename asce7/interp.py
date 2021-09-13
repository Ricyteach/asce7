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


def _twice_interp1d_with_2d_z_list(x_arr, y_arr, z_arr, x_axis, bounds_error, fill_value):

    y_axis = abs(x_axis - 1)
    axis_dict = {x_axis: x_arr, y_axis: y_arr}
    row_arr, col_arr = (axis_dict[i] for i in (0,1))
    if (row_arr.size, col_arr.size) != z_arr.shape:
        raise ValueError(f"Shape of z does not match sizes of x and y with x at axis {x_axis} of z")

    interp1d_rows = [interp1d(col_arr, row, bounds_error=bounds_error, fill_value=fill_value) for row in z_arr]

    def interpolate(x, y):
        """Interpolate the function.

         Parameters
         ----------
         x : 1-D array
             x-coordinates of the mesh on which to interpolate.
         y : 1-D array
             y-coordinates of the mesh on which to interpolate.

         Returns
         -------
         z : 2-D array with shape (len(y), len(x))
             The interpolated values.
        """

        axis_dict = {x_axis: x, y_axis: y}
        row_v, col_v = (axis_dict[i] for i in (0,1))

        temp_z = [f(col_v) for f in interp1d_rows]
        return interp1d(row_arr, temp_z, bounds_error=bounds_error, fill_value=fill_value)(x)

    return interpolate


if __name__ == "__main__":
    f = _twice_interp1d_with_2d_z_list(np.array([1,2]), np.array([1,2,3]), np.array([[1,2,3],[4,5,6]]), x_axis=0, bounds_error=False, fill_value=None)
    assert f(1.5, 1.5) == 3.0
    assert f(1, 1.5) == 1.5
    assert f(1.5, 1) == 2.5
