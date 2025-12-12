# Rocket Relations Demo

from rocket_relations.ideal import (
    c_star,
    thrust_coefficient,
    area_ratio,
    ve,
    Isp,
    m_dot,
    F_th,
    F,
)

T0 = 2900.0  # K
R = 8314.0 / 24.0  # J/(kg*K)  (since 8314 is J/(kmol*K), dividing by molar mass in kg/kmol)
gamma = 1.3
Pe = 101325.0  # Pa
Pa = 101325.0  # Pa
P0 = 5e5     # Pa

g0 = 9.81      # m/s^2

a_star = 10.0 * 1e-4  # m^2  (10 cm^2)

ar_val = area_ratio(gamma, Pe, P0)
cstar_val = c_star(gamma, R, T0)
cf_val = thrust_coefficient(gamma, Pe, Pa, P0, ar_val)

isp_val = Isp(cf_val, g0, cstar_val)
ve_val = ve(gamma, R, T0, Pe, P0)
mdot_val = m_dot(cstar_val, a_star, P0)

fth_val = F_th(P0, a_star, cf_val)
F_val = F(mdot_val, isp_val, g0)

print("Area Ratio =",ar_val)
print("C* =",cstar_val)
print("Thrust Coefficient cF =",cf_val)
print("Exhaust Velocity Ve =",ve_val)
print("Specific Impulse Isp =",isp_val)
print("Propellant Mass Flow =",mdot_val)
print("Theoretical Thrust Fth =",fth_val)
print("Thrust F =",F_val)


