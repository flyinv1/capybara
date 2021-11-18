
# %%

#### 350lb Thruster Sizing ####

from pint import UnitRegistry

# Setup pint
registry = UnitRegistry()
qty = registry.Quantity

# Initial parameters (Sutton)
thrust = qty(350, "lbf")
Pc = qty(650, "psi")
cstar = qty(1640, "m/s")
isp = qty(260, "s")
g0 = qty(32.2, "ft/s^2")

mdot = thrust * g0 / isp

print(mdot.to("lb/s"))

# Propellants 
# %%
