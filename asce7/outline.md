# ASCE 7

## Lookup Tables and Charts

### 1d Interpolator
Make a function that linearly interpolates a value from another value on a curve.
`scipy.interpolate.interp1d`

### 2d Interpolator
Make a function that twice linearly interpolates a value from a set of curves.

```markdown
Interpolate twice from many curves.

x, y and z are values used to approximate some function f: z = f(x, y) which returns an interpolated value.

Parameters
----------
x,y : array_like of numbers
    the independent data of the curve; either both 1d, or one of x and y can be 2d if z is 1d
z : array_like of numbers
    the dependent data of the curve; either 2d or if one of x or y are 2d, then 1d
axis: int (0 or 1)
    axis of 2d argument assumed to correspond to the first dependent axis:
        - first dependent axis is x if either y or z is 2d
        - first dependent axis is y if x is 2d
bounds_error : bool, optional
    if True, when interpolated values are requested outside the domain of the input data (x,y),
    a ValueError is raised. If False, then fill_value is used.
fill_value : number, optional
    If provided, the value to use for points outside the interpolation domain. If omitted (None),
    values outside the  domain are extrapolated via nearest-neighbor extrapolation.

Returns
-------
interpolator function (interpolant)
    a function that interpolates values

Raises
------
ValueError
    when unexpected or incompatible array shapes are provided
```

### Interpolator Dictionary
Make a dictionary that looks up an interpolation function. Data can be 1d or 2d.

```markdown
Parameters
----------
x : either a mapping with numerical array_like values, or a numerical array_like
    contains the 1st independent data of the curve; arrays can be 1d or 2d 
y : either a mapping with numerical array_like values, or a numerical array_like
    arrays can be 1d or 2d 
    for 1d interpolation, contains the dependent data of the curve
    for 2d interpolation, contains the 2nd independent data of the curve
z : either a mapping with numerical array_like values, or a numerical array_like
    arrays can be 1d or 2d 
    default is None (for 1d interpolation)
    for 2d interpolation, contains the dependent data of the curve

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

## Chapter 1

### Load Types - Section 1.2.2 (repeated in Section 2.2)
An `Enum` of the load types: `LoadType`.

### Risk Categories - Table 1.5-1
An `Enum` of the 4 risk categories: `Risk`.

### Importance Factors - Table 1.5-2
Lookups of the importance factors for 4 risk categories and 4 load types.

## Chapter 2

### Load Types - Section 2.2 (first mentioned in Section 1.2.2)
An `Enum` of the load types: `LoadType`.

### Load Combinations
#### Strength Design: Section 2.3
Load combos 1-7 for strength: `Strength` (sections 2.3.1 and 2.3.6)

#### ASD Design: Section 2.4
Load combos 1-10 for ASD: `ASD` (sections 2.4.1 and 2.4.5)
