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
drive_freq = 10.0 # Hz
R0 = 3.5 # Ohms
alpha =  0.008 # 1 / K
T0 = 293.15 # K
Cp = 134.0 # J / K / kg
rho = 19250.0 # kg/ m^2
radius = 0.1e-4 # m
length = 0.005 # m
volume = length*np.pi*radius**2 # m^3
area = 2*np.pi*radius*length
stefan_boltzman = 5.67e-8 
capacitance = 0.018 # F
inductance = 0.01 # H

state_initial = np.array([0.0, 0.0, T0])

t0 = 0.0
t_mid = 100.0
t_max = 110.0 
n_t = 10001
times = np.linspace(t_mid, t_max, n_t)

sol = spi.solve_ivp(rhs_LightBulb, [t0, t_max], state_initial, t_eval=times)

#state_initial = np.array([1e-6, 0.0, T0])

#sol2 = spi.solve_ivp(rhs_LightBulb, [t0, t_max], state_initial, t_eval=times)

plt.close('all')
plt.plot(sol.t, sol.y[0,:], '-r')
#plt.plot(sol2.t, sol2.y[0,:], '-b')
plt.xlabel('Time (s)')
plt.ylabel('Charge (C)')

plt.figure()
plt.plot(sol.t, sol.y[2,:], '-r')
#plt.plot(sol2.t, sol2.y[2,:], '-b')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (K)')

plt.figure()
plt.plot(sol.y[1,:], sol.y[2,:], '-r')
#plt.plot(sol2.y[1,:], sol2.y[2,:], '-b')
plt.xlabel('Current (A)')
plt.ylabel('Temperature (K)')


plt.figure()
plt.plot(sol.y[0,:], sol.y[1,:], '-r')
#plt.plot(sol2.y[1,:], sol2.y[2,:], '-b')
plt.ylabel('Current (A)')
plt.xlabel('Charge (C)')



Temp_RMS = np.sqrt(np.mean(sol.y[2,:]**2))
print('RMS Temperature: ', Temp_RMS)
Charge_RMS = np.sqrt(np.mean(sol.y[0,:]**2))
print('RMS Charge: ', Charge_RMS)
Current_RMS = np.sqrt(np.mean(sol.y[1,:]**2))
print('RMS Current: ', Current_RMS)
'''
non_dim_time = sol.t*drive_freq
non_dim_sol1 = np.copy(sol.y)
non_dim_sol1[0,:] = non_dim_sol1[0,:]/Charge_RMS
non_dim_sol1[1,:] = non_dim_sol1[1,:]/Current_RMS
non_dim_sol1[2,:] = non_dim_sol1[2,:]/Temp_RMS

non_dim_sol2 = np.copy(sol2.y)
non_dim_sol2[0,:] = non_dim_sol2[0,:]/Charge_RMS
non_dim_sol2[1,:] = non_dim_sol2[1,:]/Current_RMS
non_dim_sol2[2,:] = non_dim_sol2[2,:]/Temp_RMS

phase_diff = np.sqrt((non_dim_sol1[0,:] - non_dim_sol2[0,:])**2 + (non_dim_sol1[1,:] - non_dim_sol2[1,:])**2 + (non_dim_sol1[2,:] - non_dim_sol2[2,:])**2)
plt.figure()
plt.plot(sol.t, phase_diff, '-r')
plt.xlabel('Time (s)')
plt.ylabel('Phase Space Distance')
plt.yscale('log')
'''

plt.show()