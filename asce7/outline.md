# ASCE 7

## Lookup Tables and Charts

### 1d Interpolator
Make a function that linearly interpolates a value from another value on a curve.
`scipy.interpolate.interp1d`

### 2d Interpolator
Make a function that twice linearly interpolates a value from a set of curves.

```markdown
Parameters
----------
x,y : 1d array_like of numbers
    the independent data of the curve
z : 1d array_like of numbers
    the dependent data of the curve
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
```

### Interpolator Dictionary
Make a dictionary that looks up an interpolator.

```markdown
Parameters
----------
keys : array_like of strings
    lookup keys
input : 1d or 2d array_like of numbers
    the independent data of the curve
output : 1d array_like of numbers
    the dependent data of the curve

Returns
-------
{str : interpolator}
    a dictionary of interpolation functions

Raises
------
KeyError
    when a key error
OtherError
    when an other error
```

### Dict of Callables to Callable
A decorator that turns a function into a lookup from a dictionary and a subsequent call to its underlying interpolation callabe values.

```markdown
Parameters
----------
func : function
    a decorated function
callable_dict : {Any : callable}
    a dict of callable functions

Returns
-------
result : Any
    the result of the callable returned, and called with the args and kwargs
```
