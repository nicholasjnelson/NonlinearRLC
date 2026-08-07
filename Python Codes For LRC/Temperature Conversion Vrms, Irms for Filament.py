# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 11:14:42 2026

@author: AnthonySB2
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Physical constants ---
R0 = 5.369        # cold resistance ohms
# when alpha = R0/T0 temperature is too low around 300 Kelvin
alpha = 0.004403  # tungsten TCR near room temp
T0 = 293.15       # room temperature (K)

# --- Load data ---
dfV = pd.read_csv("E:/6.3V .15A LRC Trial/daq_output_multichannel_6.3V_0.15ARated_Bulb1.csv")
dfI = pd.read_csv("E:/6.3V .15A LRC Trial/current_output_shunt_6.3V_Bulb8.csv")

time = dfV["# Seconds"].to_numpy()
V = dfV["DAQ1/ai2"].to_numpy()
I = dfI["Current (A)"].to_numpy()

# --- AC frequency from function generator ---
f_ac = 10.0              # Hz
dt = time[1] - time[0]   # sampling interval
window = int((1/f_ac) / dt)  # samples per cycle (~0.1 s)
#rms provides the DC equivalent value for the power that should produce the same heating
def rms(x, w):
    return np.sqrt(np.convolve(x**2, np.ones(w)/w, mode='same'))

V_rms = rms(V, window)
I_rms = rms(I, window)

# avoid division by very small currents (blow up of temp)
I_rms_safe = np.where(np.abs(I_rms) < 1e-3, np.nan, I_rms)

#the DC equivalent resistance of the filament temperature T
R = V_rms / I_rms_safe

#computing the Temperature
Temperature = T0 + ((R / R0) - 1) / alpha


plt.figure(figsize=(10,5))
plt.plot(time, Temperature, color="blue")
plt.xlabel("Time (s)")
plt.ylabel("Temperature (K)")
plt.title("Tungsten Filament Temperature vs Time (10 Hz RMS)")
plt.grid(True)

# --- Export only time and temperature as CSV ---
out_df = pd.DataFrame({
    "Time (s)": time,
    "Temperature (K)": Temperature
})

out_df.to_csv("E:/6.3V .15A LRC Trial/time_temperature.csv", index=False)