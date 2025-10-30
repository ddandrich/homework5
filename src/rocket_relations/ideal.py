"""
ideal.py — Ideal Rocket Relations

This module provides simple functions for computing common ideal-rocket
performance parameters, including characteristic velocity (c*) and thrust
coefficient (C_F), under standard assumptions of isentropic, steady, and
choked flow.
"""

import numpy as np 
import matplotlib as plt
import math

#function for computing characteristic velocity

def c_star(gamma, R, T0):

    #c* calculation
    if gamma <= 1 or R <= 0 or T0 <= 0:
        raise ValueError("Invalid inputs: gamma>1, R>0, T0>0 required.")
    return math.sqrt((1/gamma) * ((gamma + 1)/2)**((gamma + 1)/(gamma - 1)) * R * T0)

def thrust_coefficient(gamma, pe_p0, pa_p0, area_ratio):

    #Compute the ideal thrust coefficient
    if gamma <= 1 or not (0 <= pe_p0 < 1) or not (0 <= pa_p0 < 1) or area_ratio < 1:
        raise ValueError("Invalid input values.") #Used LLM to help with this 
    
    term_1 = (2 * gamma**2 / (gamma - 1)) * (2 / (gamma + 1)) ** ((gamma + 1) / (gamma - 1))
    term_2 = 1 - pe_p0 ** ((gamma - 1) / gamma)
    cf_isentropic = math.sqrt(term_1 * term_2)
    cf_pressure = (pe_p0 - pa_p0) * area_ratio
    return cf_isentropic + cf_pressure
    