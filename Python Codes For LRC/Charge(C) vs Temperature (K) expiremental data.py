# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 23:47:44 2026

@author: AnthonySB2
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

'''
Driving Voltage: 10.0 V
Capacitor: 18.0 mF
Inductor: 10.0 mH
Light Bulb: 6.3 V, 0.15 A

'''

filename = "6_3V-_15A-LRC-Trial/daq_output_multichannel_6.3V_0.15ARated_Bulb1.csv"

# Load CSV
df1 = pd.read_csv(filename) #voltage
#df2 = pd.read_csv("E:/6.3V .15A LRC Trial/current_output_shunt_6.3V_Bulb8.csv") #current
#df3 = pd.read_csv("E:/6.3V .15A LRC Trial/Capacitor_Charge_Voltage_Output_10V_18Kmicrofarad_cap_6.3V_Bulb1_10milihentry_inductor.csv") #capacitor charge
#df4 = pd.read_csv("E:/6.3V .15A LRC Trial/time_temperature.csv") #temperature
# Extract current + voltage
time = df1["# Seconds"].astype(float)
V_LB = df1["DAQ1/ai2"].astype(float) #light bulb voltage 
V_Cap = df1["DAQ1/ai1"].astype(float) #capacitor voltage
V_Shunt = df1["DAQ1/ai0"].astype(float) #shunt voltage
Current = V_Shunt / 0.1 # shunt resistance = 0.1 ohm

Q_Cap = V_Cap*18e-3 # 18 mF capacitor charge

gauss_win = np.exp(-0.5*(np.linspace(-3, 3, 10)**2)) # Gaussian window for smoothing

I_smooth = np.convolve(Current, gauss_win, mode='same') / np.sum(gauss_win) # smooth current with rolling average

R_LB = V_LB / Current # light bulb resistance

R_good1 = R_LB[R_LB > 32.0]
Current_good1 = Current[R_LB > 32.0]
time_good1 = time[R_LB > 32.0]
R_good = R_good1[R_good1 < 42.0]
Current_good = Current_good1[R_good1 < 42.0]
time_good = time_good1[R_good1 < 42.0]

Temp_good = (R_good/3.5 - 1)/0.003 + 293.15

plt.plot(time_good, R_good, label="Light Bulb Resistance (Ohms)", color='b')

plt.figure()
plt.plot(Q_Cap, Current, '.r')
plt.xlabel("Capacitor Charge (C)")
plt.ylabel("Current (A)")
plt.savefig("Current_vs_Charge.png", dpi=300, bbox_inches='tight')

plt.figure()
plt.plot(Current_good, Temp_good, '.g')
plt.xlabel("Current (A)")
plt.ylabel("Temperature (K)")
plt.savefig("Current_vs_Temperature.png", dpi=300, bbox_inches='tight')


plt.show()

'''
Temperature = df4["Temperature (K)"]
# Combine into new DataFrame
out = pd.DataFrame({
    "Charge (C)": charge,
    "Temperature (K)": Temperature
})

# Extract columns
#time = df["# Seconds"]
#charge = df["Charge (C)"]   # or whatever your current column is named

# Plot
plt.figure(figsize=(10,5))
plt.plot(charge, Temperature, label="Temperature vs Charge", color="blue")

plt.xlabel("Charge (C)")
plt.ylabel("Temperature (K)")
plt.title("Temperature (K) vs Charge (C)")
plt.grid(True)
plt.legend()

plt.show()
# Save
"""
change CSV Name to Bulb # and Limit 
"""
out.to_csv("Tempetature(K)_Filamint_v_Charge(C)_18Kmicrofarad_cap_6.3V_Bulb1_10milihentry_inductor.csv", index=False)

print(out) 
'''