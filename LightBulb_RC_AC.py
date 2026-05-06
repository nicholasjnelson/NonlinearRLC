#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 14:04:54 2023

@author: njnelson
"""

import numpy as np
import numpy.fft as npf
import scipy.integrate as spi
import matplotlib.pyplot as plt

def V_of_t(time):
    
    return V0*np.sin(2.0*np.pi*1*time)

def rhs_LightBulb(t, state):
    charge = state[0]
    temperature = state[1]
    
    R_of_T = R0*(1.0+alpha*(temperature - T0))
    
    dT_coef = rho*volume*Cp
    
    current = (V_of_t(t) - charge/capacitance)/R_of_T
    
    rhs= np.zeros(2)
    rhs[0] = current
    rhs[1] = (current**2*R_of_T - area*stefan_boltzman*temperature**4)/dT_coef
    
    return rhs


V0 = 10.0 # V
R0 = 10.0 # Ohms
alpha =  0.004403 # 1 / K
T0 = 293.15 # K
Cp = 134.0 # J / K / kg
rho = 19250.0 # kg/ m^2
radius = 0.8e-5 # m
volume = 0.2*np.pi*radius**2 # m^3
area = 2*np.pi*radius*0.2
stefan_boltzman = 5.67e-8
capacitance = 0.025

state_initial = np.array([0.0, T0])

t0 = 0.0
t_mid = 100.0
t_max = 1100.0 
n_t = 300001
times = np.linspace(t_mid, t_max, n_t)

sol = spi.solve_ivp(rhs_LightBulb, [t0, t_max], state_initial, t_eval=times)

plt.close('all')
plt.plot(sol.t, sol.y[0,:], '-r')
plt.xlabel('Time (s)')
plt.ylabel('Charge (C)')

plt.figure()
plt.plot(sol.t, sol.y[1,:], '-b')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (K)')

R_of_T = R0*(1.0+alpha*(sol.y[1,:] - T0))
current = (V_of_t(sol.t) - sol.y[0,:]/capacitance)/R_of_T

plt.figure()
plt.plot(current[n_t//2:], R_of_T[n_t//2:], '-m')
plt.ylabel('Resistance (Omhs)')
plt.xlabel('Current (A)')

plt.figure()
plt.plot(sol.t, current, '-g')
plt.xlabel('Time (s)')
plt.ylabel('Current (A)')

plt.figure()
plt.plot(sol.y[0,:], sol.y[1,:], '*k')
plt.ylabel('Temperature (K)')
plt.xlabel('Charge (C)')


Q_spec = npf.rfft(sol.y[0,:])
freqs = npf.rfftfreq(len(sol.y[0,:]), d=times[1]-times[0])

plt.figure()
plt.plot(freqs, np.abs(Q_spec)**2)
plt.yscale('log')

plt.show()






