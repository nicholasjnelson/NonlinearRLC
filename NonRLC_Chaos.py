import numpy as np
import numpy.fft as npf
import scipy.integrate as spi
import matplotlib.pyplot as plt


def rhs_LightBulb(time, state, params):
    charge = state[0]
    current = state[1]
    temperature = state[2]

    V0, drive_freq, R0, radius, length, capacitance, inductance = params
    volume = np.pi*radius**2*length
    area = 2*np.pi*radius*length

    R_of_T = R0*(1.0+alpha*(temperature - T0))
    
    dT_coef = rho*volume*Cp
    
    rhs= np.zeros(3)
    rhs[0] = current
    rhs[1] = (V0*np.sin(2.0*np.pi*drive_freq*time) - charge/capacitance - current*R_of_T)/inductance
    rhs[2] = (current**2*R_of_T - area*stefan_boltzman*temperature**4)/dT_coef
    
    return rhs

def NonRLC_PhaseSpaceDist(params, state_initial, times):
    sol = spi.solve_ivp(rhs_LightBulb, [t0, t_max], state_initial, args=(params,), t_eval=times)
    state_initial = state_initial + np.array([0.1, 0.1, 1000])*np.random.normal(0.0, 1e-6, size=state_initial.shape)
    sol2 = spi.solve_ivp(rhs_LightBulb, [t0, t_max], state_initial, args=(params,), t_eval=times)


    Temp_RMS = np.sqrt(np.mean(sol.y[2,:]**2))
    Charge_RMS = np.sqrt(np.mean(sol.y[0,:]**2))
    Current_RMS = np.sqrt(np.mean(sol.y[1,:]**2))

    non_dim_sol1 = np.copy(sol.y)
    non_dim_sol1[0,:] = non_dim_sol1[0,:]/Charge_RMS
    non_dim_sol1[1,:] = non_dim_sol1[1,:]/Current_RMS
    non_dim_sol1[2,:] = non_dim_sol1[2,:]/Temp_RMS

    non_dim_sol2 = np.copy(sol2.y)
    non_dim_sol2[0,:] = non_dim_sol2[0,:]/Charge_RMS
    non_dim_sol2[1,:] = non_dim_sol2[1,:]/Current_RMS
    non_dim_sol2[2,:] = non_dim_sol2[2,:]/Temp_RMS

    phase_diff = np.sqrt((non_dim_sol1[0,:] - non_dim_sol2[0,:])**2 + (non_dim_sol1[1,:] - non_dim_sol2[1,:])**2 + (non_dim_sol1[2,:] - non_dim_sol2[2,:])**2)

    return phase_diff


# Fixed parameters
alpha =  0.004403 # 1 / K
T0 = 293.15 # K
Cp = 134.0 # J / K / kg
rho = 19250.0 # kg/ m^2
stefan_boltzman = 5.67e-8 

# Variable parameters
V0 = 20.0 # V
drive_freq = 0.2 # Hz
R0 = 1.0 # Ohms
radius = 0.5e-4 # m
length = 0.001 # m
capacitance = 0.025 # F
inductance = 0.6 # H

# Initial conditions
state_initial = np.array([0.0, 0.0, T0])

# Time parameters
t0 = 0.0
t_max = 100.0
n_t = 100001
times = np.linspace(t0, t_max, n_t)

n_search = 5

max_phase_dists = np.zeros([n_search,n_search, n_search])
max_pd = 0.0
capacitances = np.linspace(0.1, 1.0, n_search)
inductances = np.linspace(0.1, 1.0, n_search)
drive_freqs = np.linspace(0.1, 1.0, n_search)

for i in range(n_search):
    print('Drive Freq: ', drive_freqs[i])
    for j in range(n_search):
        for k in range(n_search):
            params = (V0, drive_freqs[i], R0, radius, length, capacitances[j], inductances[k])
            phase_diff = NonRLC_PhaseSpaceDist(params, state_initial, times)
            max_phase_dists[i,j,k] = np.max(phase_diff)
            if max_phase_dists[i,j,k] > max_pd:
                max_pd = max_phase_dists[i,j,k]
                print('Drive Freq: ', drive_freqs[i], ' Capacitance: ', capacitances[j], ' Inductance: ', inductances[k], ' Max Phase Dist: ', max_phase_dists[i,j,k])



