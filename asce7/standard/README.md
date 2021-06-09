# Standards Module

I have not been satisfied with existing tools I have found for the creation of tables, charts, and figures typically
found in engineering standards, which require quite a bit of flexible interpolation.

This module is my take on what such tools should look like. The primary application is interpolation of various
standards from engineering building and design codes (hence the class name, `StandardLookup`). However, I have other 
applications in mind (such as visual display of interpolation in charts and tables).

```python
# Example

from asce7.standard import StandardLookup
import pandas as pd


rows = ["A", "B"]
subrows = ["1", "2"]
x = [1, 2]
y = [10, 20, 30]
z = [
    # _X=1_    |    _X=2_
# Y= 10 20  30 | 10  20  30
# A1             
    [ 1, 2,  3,   4,  5,  6],
# A2              
    [ 2, 4,  6,   8, 10, 12],
# B1              
    [ 3, 6,  9,  12, 15, 18],
# B2             
    [ 4, 8, 12,  16, 20, 24],
]
index = pd.MultiIndex.from_product([rows, subrows])
xy_standard = StandardLookup(x=x, y=y, z=z, index=index)
assert xy_standard.lookup[("B", "1")](1.5, 25) == 16
```
