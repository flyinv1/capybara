
# %%

#### Thruster Sizing ####

import numpy as np
from modules.units import qty

# Initial parameters (Sutton)
thrust = qty(500, "lbf").to("N")
burn_time = qty(20, "s")
Pc = qty(500, "psi")
cstar = qty(1640, "m/s")
isp = qty(200, "s")
g0 = qty(9.80665, "m/s^2")
OF = 1.35

mdot = thrust / (isp * g0)
prop_mass = burn_time * mdot

lox_mass = prop_mass.to("kg") / ( 1 + 1 / OF )
ipa_mass = prop_mass.to("kg") / ( 1 + OF )

print("mass flow: ", mdot.to("kg/s"))

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

from modules.stress import fos, hoop, longitudinal

P_tank = qty(900, "psi")
thickness = qty(0.25, "in")
r_outer = qty(4, "in")
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

print("tank OD: ", (r_outer * 2).to("in"))
print("lox tank length: ", min_lox_tank_length.to("in"))
print("ipa tank length: ", min_ipa_tank_length.to("in"))

ipa_tank_mass = ((np.pi * r_outer ** 2 - np.pi * r_inner ** 2) * min_ipa_tank_length + cap_thickness * 2 * np.pi * r_outer ** 2 ) * al_6061_rho
lox_tank_mass = ((np.pi * r_outer ** 2 - np.pi * r_inner ** 2) * min_lox_tank_length + cap_thickness * 2 * np.pi * r_outer ** 2 ) * al_6061_rho

print("lox tank mass: ", lox_tank_mass.to("lb"))
print("ipa tank mass: ", ipa_tank_mass.to("lb"))


# %% 

#### Altitude Requirements ####

ms = qty(40, "lb") + ipa_tank_mass + lox_tank_mass
m0 = ms + prop_mass
mr = m0 / ms

print("mass ratio: ", mr)
print("takoff T/W: ", (thrust / (g0 * m0)).to_base_units())

dv = isp * g0 * np.log(mr)

cross_area = np.pi * r_outer ** 2
Cd = qty(0.4, "dimensionless")
rho_sea_air = qty(1.116, "kg/m^3")
# Todo: 
# [ ] convert drag to function of velocity
# [ ] add wave drag in transonic regime
# [ ] add Cd function
vavg = qty(450, "m/s")
drag = 1 / 2 * Cd * rho_sea_air * (vavg / 2) ** 2 * cross_area

v = lambda t: ((thrust - drag) / (m0 - mdot * t) - g0) * t
z = lambda t: 1 / 2 * ((thrust - drag) / (m0 - mdot * t) - g0) * t ** 2

vb = v(burn_time)
zb = z(burn_time)
zc = 1 / 2 * vb ** 2 / g0

print("burnout:", zb.to("mi"))
print("coast:", zc.to("mi"))
print("max altitude:", (zb + zc).to("mi"))
print("burnout velocity:", vb.to("mph"))
print("drag:", drag.to("N"))

# %%

#### Engine Parameters ####

Pa = qty(13.3, "psi")
Pe = Pa # Optimize for 4000ft performance

Pr = Pc / Pe
AR = 5 # Area ratio for ideal expansion (k = 1.2)

At = mdot * cstar / (Pc)
Ae = At * AR
Cf = thrust / (Pc * At)
rt = np.sqrt(At / np.pi)
re = np.sqrt(Ae / np.pi)
dt = 2 * rt
de = 2 * re
rho_prop = lox_rho / (1 + 1 / OF) + ipa_rho / (1 + OF)
vol_ratio = lox_vol / ipa_vol

print("Average density:", rho_prop)
print("Volume ratio", vol_ratio)

contraction_ratio = 3
Ac = contraction_ratio * At # Chamber Area
rc = np.sqrt(Ac / np.pi)

Lstar = qty(15, "in") # From SP-125 for RP-1 - conservative for IPA
Vc = Lstar * At
ts = Vc / (1 / rho_prop * mdot)
contraction_half_angle = qty(45, "degrees")

Lc_cyl = (Vc / At - 1 / 3 * np.sqrt(At / np.pi) * 1 / np.tan(contraction_half_angle.to("rad")) * (contraction_ratio ** (1 / 3) - 1)) / contraction_ratio
Lc_contraction = np.tan(contraction_half_angle.to("rad")) * (rc - rt)

print('chamber length:', Lc_cyl.to("in"))
print('converging length:', Lc_contraction.to("in"))
print("chamber vol:", Vc.to("L"))
print("stay time:", ts.to("s"))

print()

print("PR:", Pr)
print("Cf:", Cf)
print("Throat area:", At.to("in^2"))
print("Throat diameter:", dt.to("in"))
print("Exit area:", Ae.to("in^2"))
print("Exit diameter:", de.to("in"))



# %%
