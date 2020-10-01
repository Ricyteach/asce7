# ASCE 7

This project is not intended to fully replicate the entire ASCE 7 buildling code, only the parts I find useful.

Proposed, example API (not yet implemented):

```python
# Example calculation module

import asce7.chapter1 as ch1
import asce7.chapter7 as ch7
from asce7.chapter2.load_combination import asd as asd_combo, strength as strn_combo

risk = ch1.risk_category("II")  # or
risk = ch1.risk_category(2)  # or
risk = ch1.risk_category.II

# Snow importance factor
I_s = ch7.I_s(risk)

# Ground snow load
p_g = ch7.p_g(20)

# Surface roughness
rgh = ch7.roughness("B")  # or
rgh = ch7.roughness.B

# Roof exposure
exp = ch7.roof_exposure("Fully")  # or
exp = ch7.roof_exposure.fully

# Snow exposure factor
C_e = ch7.C_e(rgh, exp)

# Snow thermal condition
thrml = ch7.thermal_condition("unheated open air")  # or
thrml = ch7.thermal_condition.unheated_open_air

# Snow thermal factor
C_t = ch7.C_t(thrml)

# Flat roof snow load
p_f = ch7.p_f(C_e, C_t, I_s, p_g)

# Some load combinations including snow
strn2 = strn_combo[2](S = p_f)
strn3 = strn_combo[3](S = p_f)
asd3 = asd_combo[3](S = p_f)
asd6 = asd_combo[6](S = p_f)
```
