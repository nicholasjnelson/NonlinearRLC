import numpy as np
import numpy.fft as npf
import scipy.integrate as spi
import matplotlib.pyplot as plt

def V_of_t(time):
    
    return V0*np.sin(2.0*np.pi*drive_freq*time)

def rhs_LightBulb(t, state):
    charge = state[0]
    current = state[1]
    temperature = state[2]
    
    R_of_T = R0*(1.0+alpha*(temperature - T0))
    
    dT_coef = rho*volume*Cp
    
    rhs= np.zeros(3)
    rhs[0] = current
    rhs[1] = (V_of_t(t) - charge/capacitance - current*R_of_T)/inductance
    rhs[2] = (current**2*R_of_T - area*stefan_boltzman*temperature**4)/dT_coef
    
    return rhs


V0 = 10.0 # V
drive_freq = 0.5 # Hz
R0 = 10.0 # Ohms
alpha =  0.004403 # 1 / K
T0 = 293.15 # K
Cp = 134.0 # J / K / kg
rho = 19250.0 # kg/ m^2
radius = 0.8e-5 # m
volume = 0.2*np.pi*radius**2 # m^3
area = 2*np.pi*radius*0.2
stefan_boltzman = 5.67e-8 
capacitance = 0.025 # F
inductance = 0.6 # H

state_initial = np.array([0.0, 0.0, T0])

t0 = 0.0
t_mid = 100.0
t_max = 200.0 
n_t = 10001
times = np.linspace(t_mid, t_max, n_t)

sol = spi.solve_ivp(rhs_LightBulb, [t0, t_max], state_initial, t_eval=times)

plt.close('all')
plt.plot(sol.t, sol.y[0,:], '-r')
plt.xlabel('Time (s)')
plt.ylabel('Charge (C)')

plt.figure()
plt.plot(sol.t, sol.y[2,:], '-b')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (K)')

plt.figure()
plt.plot(sol.y[1,:], sol.y[2,:], '-g')
plt.xlabel('Current (A)')
plt.ylabel('Temperature (K)')

plt.show()