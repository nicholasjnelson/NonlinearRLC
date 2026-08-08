import numpy as np
import scipy.optimize as spo
import matplotlib.pyplot as plt
import scipy.integrate as spi
import scipy.constants as spc
import datetime

rho_x_Cp = 19250.0*134.0 # kg/m^3 * J/kg/K for tungsten
T0 = 293.15 # K

def rhs_LightBulb(time, state, params):
    charge = state[0]
    current = state[1]
    temperature = state[2]

    V0, drive_freq, R0, alpha, R_stray, radius, length, capacitance, inductance, phase_shift = params
    volume = np.pi*radius**2*length
    area = 2*np.pi*radius*length

    R_of_T = R0*(1.0+alpha*(temperature - T0))
    
    dT_coef = rho_x_Cp*volume
    
    rhs= np.zeros(3)
    rhs[0] = current
    rhs[1] = (V0*np.sin(2.0*np.pi*drive_freq*time + phase_shift) - charge/capacitance - current*(R_of_T + R_stray))/inductance
    rhs[2] = (current**2*R_of_T - area*spc.sigma*temperature**4)/dT_coef
    
    return rhs

data = np.loadtxt("6_3V-_15A-LRC-Trial/daq_output_multichannel_6.3V_0.15ARated_Bulb1.csv", delimiter= ",", skiprows=1)
time = data[:1000,0] + 15.0
V_shunt = data[:1000,1]
V_cap = data[:1000,2] - np.mean(data[:,2]) # subtract mean to remove offset
V_LB = data[:1000,3]

current = V_shunt / 0.1 # shunt resistance = 0.1 ohm

params = np.zeros(10)
params[0] = 10.0  # V0
params[1] = 10.0  # drive_freq
params[2] = 3.795  # R0
params[3] = 0.00285  # alpha
params[4] = 5.0  # Stray linear resistance
params[5] = 9.108e-5  # radius
params[6] = 1.414e-4  # length
params[7] = 0.018  # capacitance
params[8] = 0.01  # inductance
params[9] = -2.622  # phase_shift

state_initial = np.array([0.0, 0.0, T0])

sol = spi.solve_ivp(rhs_LightBulb, [0, time[-1]], state_initial, args=(params,), t_eval=time)

plt.plot(time, current, label="Experiment", color='r')
plt.plot(time, sol.y[1,:], label="Model", color='b')
plt.xlabel("Time (s)")
plt.ylabel("Current (A)")
plt.legend()

plt.figure()
plt.plot(time, V_cap, label="Experiment", color='r')
plt.plot(time, sol.y[0,:]/params[7], label="Model", color='b')
plt.xlabel("Time (s)")
plt.ylabel("Capacitor Voltage (V)")
plt.legend()

plt.figure()
plt.plot(time, V_LB, label="Experiment", color='r')
plt.plot(time, sol.y[1,:]*params[2]*(1.0+params[3]*(sol.y[2,:] - T0)), label="Model", color='b')
plt.xlabel("Time (s)")
plt.ylabel("Light Bulb Voltage (V)")
plt.legend()

plt.figure()
plt.plot(V_cap*params[7], current, label="Experiment", color='r')
plt.plot(-sol.y[0,:], sol.y[1,:], label="Model", color='b')
plt.xlabel("Charge (C)")
plt.ylabel("Current (A)")
plt.legend()

plt.figure()
plt.plot(current, V_LB/current, label="Experiment", color='r', marker='.', linestyle='None')
plt.plot(sol.y[1,:], params[2]*(1.0+params[3]*(sol.y[2,:] - T0)), label="Model", color='b')   
plt.xlabel("Current (A)")
plt.ylabel(r"Resistance ($\Omega$)")
plt.legend()

plt.show()
