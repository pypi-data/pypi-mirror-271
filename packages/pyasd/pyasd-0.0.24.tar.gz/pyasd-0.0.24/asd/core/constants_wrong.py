#!/usr/bin/env python

#!==========================================
# THIS script is WRONG!!!!!!
#===========================================


# physical constants for spin dynamics simulations
# Shunhong Zhang
# May 19, 2021

import numpy as np
from scipy.constants import physical_constants 


mu_0 = physical_constants['vacuum mag. permeability'][0]
e_chg = physical_constants['elementary charge'][0]
kB = physical_constants['Boltzmann constant in eV/K'][0]*1e3
gamma_e = physical_constants['electron gyromag. ratio'][0]
muB = physical_constants['Bohr magneton in eV/T'][0]*1e3
PlanckConstant = physical_constants['Planck constant in eV/Hz'][0]
Hbar = PlanckConstant / (2*np.pi)


# Data from wikipedia, for references
"""
mu_0 = 2.0133545e2                  # vacuum permeability, in T^2*Angstrom^3/meV
e_chg = 1.6021766e-19               # elementary charge in Coulomb
kB = 8.617333262145e-2              # Boltzmann constant, in meV/K
gamma_e = 0.1760859644              # electron gyromagnetic ratio, in rad/T/ps
muB = 0.057883817555                # Bohr Magnetom, in utit of meV/T
PlanckConstant = 4.13566733e-15     # [eV s]
Hbar = PlanckConstant/(2*np.pi)     # [eV s]
"""


if __name__=='__main__':
    keys = [
    'vacuum mag. permeability',
    'elementary charge',
    'Boltzmann constant in eV/K',
    'electron gyromag. ratio',
    'Bohr magneton in eV/T',
    'Planck constant in eV/Hz']
    for key in keys: print( '{:<30s} {}'.format(key, physical_constants[key]))
 
