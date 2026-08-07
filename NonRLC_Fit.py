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

def NonRLC_FitData(fit_params, times, exp_data, set_params):

    # fit params = [R0, alpha, radius, length, , phase_shift]
    # set_params = [V0, drive_freq, R_stray, capacitance, inductance]

    data_current = exp_data[0,:]
    RMS_data_current = np.sqrt(np.mean(data_current**2))
    data_V_cap = exp_data[1,:]
    RMS_data_V_cap = np.sqrt(np.mean(data_V_cap**2))
    data_V_LB = exp_data[2,:]
    RMS_data_V_LB = np.sqrt(np.mean(data_V_LB**2))

    params = np.zeros(10)
    params[0] = set_params[0]  # V0
    params[1] = set_params[1]  # drive_freq
    params[2] = fit_params[0]  # R0
    params[3] = fit_params[1]  # alpha
    params[4] = fit_params[2]  # Stray linear resistance
    params[5] = fit_params[3]  # radius
    params[6] = fit_params[4]  # length
    params[7] = set_params[2]  # capacitance
    params[8] = set_params[3]  # inductance
    params[9] = fit_params[5]  # phase_shift


    state_initial = np.array([0.0, 0.0, T0])

    sol = spi.solve_ivp(rhs_LightBulb, [0, times[-1]], state_initial, args=(params,), t_eval=times)

    time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("ODE solver success: ", sol.success, " ", time_str)
    if not sol.success:
        print("ODE solver failed with message: ", sol.message)
        print("V0 = ", params[0], " drive_freq = ", params[1], " R0 = ", params[2], " alpha = ", params[3], " radius = ", params[4], " length = ", params[5], " capacitance = ", params[6], " inductance = ", params[7], " phase_shift = ", params[8])
    model_current = sol.y[1,:]
    model_V_cap = sol.y[0,:]/params[6]
    model_V_LB = model_current*params[2]*(1.0+params[3]*(sol.y[2,:] - T0))

    RMS_diff = np.sqrt(np.mean((model_current - data_current)**2)/ RMS_data_current**2 + 
                       np.mean((model_V_cap - data_V_cap)**2)/RMS_data_V_cap**2 + 
                       np.mean((model_V_LB - data_V_LB)**2)/RMS_data_V_LB**2)
    
    return RMS_diff

# Import data

data = np.loadtxt("6_3V-_15A-LRC-Trial/daq_output_multichannel_6.3V_0.15ARated_Bulb1.csv", delimiter= ",", skiprows=1)
time = data[:1000,0] + 15.0
V_shunt = data[:1000,1]
V_cap = data[:1000,2] - np.mean(data[:,2]) # subtract mean to remove offset
V_LB = data[:1000,3]

current = V_shunt / 0.1 # shunt resistance = 0.1 ohm

exp_data = np.zeros((3, len(time)))
exp_data[0,:] = current
exp_data[1,:] = V_cap
exp_data[2,:] = V_LB    

fixed_params = [10.0, 10.0, 0.018, 0.01] # V0, drive_freq, capacitance, inductance
guess_params = [3.795, 0.00285, 5.0, 9.108e-5, 1.414e-4,  -2.622] # R0, alpha, R_stray, radius, length, phase_shift

bounds = [(2.0, 8.0), (0.0001, 0.02), (0.0, 15.0),(1e-5, 0.01), (1e-5, 0.01), (-np.pi, np.pi)] # bounds for R0, alpha, radius, length, capacitance, inductance, phase_shift

min_result = spo.minimize(NonRLC_FitData, guess_params, args=(time, exp_data, fixed_params), method='Powell', 
                          bounds=bounds, options={'maxiter': 100, 'disp': True})

print("Convergence status: ", min_result.success)
print("Minimization Message: ", min_result.message)
print("Best fit parameters: ", min_result.x)
print("Best fit function value: ", min_result.fun)
#print("Covariance matrix: ", min_result.hess_inv) # Hessian inverse is not available for Powell method

params = np.zeros(10)
params[0] = fixed_params[0]  # V0
params[1] = fixed_params[1]  # drive_freq
params[2] = min_result.x[0]  # R0
params[3] = min_result.x[1]  # alpha
params[4] = min_result.x[2]  # R_stray
params[5] = min_result.x[3]  # radius
params[6] = min_result.x[4]  # length
params[7] = fixed_params[2]  # capacitance
params[8] = fixed_params[3]  # inductance
params[9] = min_result.x[5]  # phase_shift

sol_best = spi.solve_ivp(rhs_LightBulb, [0, time[-1]], np.array([0.0, 0.0, T0]), args=(params,), t_eval=time)

plt.plot(time, current, label="Experiment", color='r')
plt.plot(time, sol_best.y[1,:], label="Model", color='b')
plt.xlabel("Time (s)")
plt.ylabel("Current (A)")
plt.legend()

plt.figure()
plt.plot(time, V_cap, label="Experiment", color='r')
plt.plot(time, sol_best.y[0,:]/params[6], label="Model", color='b')
plt.xlabel("Time (s)")
plt.ylabel("Capacitor Voltage (V)")
plt.legend()

plt.figure()
plt.plot(time, V_LB, label="Experiment", color='r')
plt.plot(time, sol_best.y[1,:]*params[2]*(1.0+params[3]*(sol_best.y[2,:] - T0)), label="Model", color='b')
plt.xlabel("Time (s)")
plt.ylabel("Light Bulb Voltage (V)")
plt.legend()

plt.figure()
plt.plot(V_cap*params[6], current, label="Experiment", color='r')
plt.plot(-sol_best.y[0,:], sol_best.y[1,:], label="Model", color='b')
plt.xlabel("Charge (C)")
plt.ylabel("Current (A)")
plt.legend()

plt.figure()
plt.plot(current, V_LB/current, label="Experiment", color='r', marker='.', linestyle='None')
plt.plot(sol_best.y[1,:], params[2]*(1.0+params[3]*(sol_best.y[2,:] - T0)), label="Model", color='b')   
plt.xlabel("Current (A)")
plt.ylabel(r"Resistance ($\Omega$)")
plt.legend()

plt.show()
