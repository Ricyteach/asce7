# ASCE 7

## Lookup Tables and Charts

### 1d Interpolator
Make a function that linearly interpolates a value from another value on a curve.
`scipy.interpolate.interp1d`

### 2d Interpolator
Make a function that linearly interpolates a value from a pair of coordinate values on a surface.
`scipy.interpolate.interp2d`

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
