
# %%

#### Thruster Sizing ####

import numpy as np
from modules.units import qty

# Initial parameters (Sutton)
thrust = qty(350, "lbf").to("N")
burn_time = qty(20, "s")
Pc = qty(500, "psi")
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

print("lox vol: ", lox_vol.to("in^3"))
print("ipa vol: ", ipa_vol.to("in^3")) 

# %%

#### Tank Sizing ####

from modules.stress import fos, hoop, longitudinal

P_tank = qty(900, "psi")
thickness = qty(0.25, "in")
r_outer = qty(2.5, "in")
r_inner = r_outer - 2 * thickness
cap_thickness = qty(1, "in")
al_6061T6_yield = qty(35000, "psi")
al_6061_rho = qty(2.70, "g/cm^3")

hoop_fos = fos(al_6061T6_yield, hoop(P_tank, (r_inner + r_outer) / 2, thickness))
long_fos = fos(al_6061T6_yield, longitudinal(P_tank, (r_inner + r_outer) / 2, thickness))

print("hoop fos: ", hoop_fos)
print("long fos: ", long_fos)

min_lox_tank_length = lox_vol / (np.pi * r_inner ** 2) 
min_ipa_tank_length = ipa_vol / (np.pi * r_inner ** 2)

print("lox tank length: ", min_lox_tank_length.to("in"))
print("ipa tank length: ", min_ipa_tank_length.to("in"))

ipa_tank_mass = ((np.pi * r_outer ** 2 - np.pi * r_inner ** 2) * min_ipa_tank_length + cap_thickness * 2 * np.pi * r_outer ** 2 ) * al_6061_rho
lox_tank_mass = ((np.pi * r_outer ** 2 - np.pi * r_inner ** 2) * min_lox_tank_length + cap_thickness * 2 * np.pi * r_outer ** 2 ) * al_6061_rho

print("lox tank mass: ", lox_tank_mass.to("lb"))
print("ipa tank mass: ", ipa_tank_mass.to("lb"))

# %% 

#### Altitude Requirements ####

m0 = qty(90, "lb")
mf = m0 - prop_mass

dv = isp * g0 * np.log(m0 / mf) - g0 * burn_time

print("dv: ", dv.to("m/s"))

# %%

