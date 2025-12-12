"""
ideal.py — Ideal Rocket Relations

This module provides simple functions for computing common ideal-rocket
performance parameters, including characteristic velocity (c*), area_ratio, thrust
coefficient (C_F), specific impulse (ISP), exhaust velocity (ve), propellant mass flow (m_dot), and thrust under standard assumptions of isentropic, steady, and
choked flow.

*Note: This package can be used for rockets designed at sea level (Pe=Pa) and for back pressure conditions (Pe=/Pa)
"""

import numpy as np
import math


# function for computing characteristic velocity
def c_star(gamma, R, T0):

    # convert inputs (allows numpy arrays)
    gamma = np.asarray(gamma)
    R = np.asarray(R)
    T0 = np.asarray(T0)

    # c_star calculation
    if np.any(gamma <= 1) or np.any(R <= 0) or np.any(T0 <= 0):
        raise ValueError("Invalid inputs: gamma>1, R>0, T0>0 required.")
    else:
        return np.sqrt((1 / gamma) * ((gamma + 1) / 2) ** ((gamma + 1) / (gamma - 1)) * R * T0)


# function for computing thrust coefficient
def thrust_coefficient(gamma, Pe, Pa, P0, area_ratio):

    # convert inputs (allows numpy arrays)
    gamma = np.asarray(gamma)
    Pe = np.asarray(Pe)
    Pa = np.asarray(Pa)
    P0 = np.asarray(P0)
    area_ratio = np.asarray(area_ratio)

    # Compute pe_p0 and pa_p0 ratios
    pe_p0 = Pe / P0
    pa_p0 = Pa / P0

    # Compute the ideal thrust coefficient for back pressure conditions
    if np.any(gamma <= 1) or np.any((pe_p0 < 0) | (pe_p0 >= 1)) or np.any((pa_p0 < 0) | (pa_p0 >= 1)) or np.any(area_ratio < 1):
        raise ValueError("Invalid input values.")
    else:
        term_1 = (2 * gamma**2 / (gamma - 1)) * (2 / (gamma + 1)) ** ((gamma + 1) / (gamma - 1))
        term_2 = 1 - pe_p0 ** ((gamma - 1) / gamma)
        cf_isentropic = np.sqrt(term_1 * term_2)

        # if Pe == Pa, return isentropic-only
        if np.all(Pe == Pa):
            return cf_isentropic
        else:
            cf_pressure = (pe_p0 - pa_p0) * area_ratio
            return cf_isentropic + cf_pressure


# function for computing area ratio
def area_ratio(gamma, Pe, P0):

    # convert inputs (allows numpy arrays)
    gamma = np.asarray(gamma)
    Pe = np.asarray(Pe)
    P0 = np.asarray(P0)

    # Compute the area ratio for back pressure conditions
    if np.any(gamma <= 1) or np.any(Pe <= 0) or np.any(P0 <= 0):
        raise ValueError("Invalid input values.")
    else:
        term_a_1 = np.sqrt((gamma - 1) / 2) * ((2) / gamma + 1) ** ((gamma + 1) / (2 * (gamma - 1)))
        term_a_2 = (Pe / P0) ** (1 / gamma)
        term_a_3 = np.sqrt(1 - (Pe / P0) ** ((gamma - 1) / gamma))
        area_ratio = term_a_1 * (1 / (term_a_2 * term_a_3))
        return area_ratio


# function for computing specific impulse (Isp)
def Isp(cf, g0, c_star):

    # convert inputs (allows numpy arrays)
    cf = np.asarray(cf)
    g0 = np.asarray(g0)
    c_star = np.asarray(c_star)

    # check for valid inputs
    if np.any(c_star <= 0) or np.any(g0 <= 0):
        raise ValueError("Invalid input values.")
    else:
        return (c_star * cf) / g0


# function for computing exhaust velocity (ve)
def ve(gamma, R, T0, Pe, P0):

    # convert inputs (allows numpy arrays)
    gamma = np.asarray(gamma)
    R = np.asarray(R)
    T0 = np.asarray(T0)
    Pe = np.asarray(Pe)
    P0 = np.asarray(P0)

    # Calculate pressure ratio
    pe_p0 = Pe / P0

    # Compute the exhaust velocity
    if np.any(gamma <= 1) or np.any((pe_p0 < 0) | (pe_p0 >= 1)) or np.any(T0 <= 0) or np.any(R <= 0):
        raise ValueError("Invalid input values.")
    else:
        return np.sqrt(2 * (gamma / (gamma - 1)) * R * T0 * (1 - (pe_p0) ** ((gamma - 1) / gamma)))


# function for computing mass flow (m_dot)
def m_dot(c_star, a_star, P0):

    # convert inputs (allows numpy arrays)
    c_star = np.asarray(c_star)
    a_star = np.asarray(a_star)
    P0 = np.asarray(P0)

    # Compute propellant mass flow rate
    if np.any(P0 <= 0) or np.any(c_star <= 0) or np.any(a_star <= 0):
        raise ValueError("Invalid input values.")
    else:
        return (P0 * a_star) / c_star


# function for computing theoretical thrust via cF
def F_th(P0, a_star, cf):

    # convert inputs (allows numpy arrays)
    P0 = np.asarray(P0)
    a_star = np.asarray(a_star)
    cf = np.asarray(cf)

    # Compute theoretical thrust
    if np.any(P0 <= 0) or np.any(cf <= 0) or np.any(a_star <= 0):
        raise ValueError("Invalid input values.")
    else:
        return cf * P0 * a_star


# function for computing actual thrust using m_dot
def F(m_dot, Isp, g0):

    # convert inputs (allows numpy arrays)
    m_dot = np.asarray(m_dot)
    Isp = np.asarray(Isp)
    g0 = np.asarray(g0)

    # Compute thrust
    if np.any(m_dot <= 0) or np.any(Isp <= 0) or np.any(g0 <= 0):
        raise ValueError("Invalid input values.")
    else:
        return m_dot * Isp * g0




    
    