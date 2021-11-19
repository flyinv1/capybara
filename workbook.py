
# %%

#### 350lb Thruster Sizing ####

import numpy as np
from pint import UnitRegistry

# Setup pint
registry = UnitRegistry()
qty = registry.Quantity

# Initial parameters (Sutton)
thrust = qty(350, "lbf").to("N")
burn_time = qty(20, "s")
Pc = qty(650, "psi")
cstar = qty(1640, "m/s")
isp = qty(260, "s")
g0 = qty(9.80665, "m/s^2")
OF = 1.35

mdot = thrust / (isp * g0)
prop_mass = burn_time * mdot

lox_mass = prop_mass.to("kg") / ( 1 + 1 / OF )
ipa_mass = prop_mass.to("kg") / ( 1 + OF )

print("lox mass: ", lox_mass)
print("ipa mass: ", ipa_mass)

lox_rho = qty(1134, "kg/m^3")
ipa_rho = qty(786, "kg/m^3")

lox_vol = lox_mass / lox_rho
ipa_vol = ipa_mass / ipa_rho

print("lox vol: ", lox_vol.to("L"))
print("ipa vol: ", ipa_vol.to("L")) 

# %%

#### Tank Sizing ####

# %% 

#### Altitude Requirements ####

m0 = qty(90, "lb")
mf = m0 - prop_mass

dv = isp * g0 * np.log(m0 / mf) - g0 * burn_time

print("dv: ", dv.to("m/s"))

# %%

