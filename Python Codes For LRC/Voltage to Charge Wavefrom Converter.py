# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 22:59:18 2026

@author: AnthonySB2
"""

import pandas as pd
import matplotlib.pyplot as plt
# Load CSV
"""
---->DAQ Channel ai1 is capacitor <-----
"""
#copy file path 
df = pd.read_csv("E:/6.3V .15A LRC Trial/daq_output_multichannel_6.3V_0.15ARated_Bulb1.csv")

# Extract time + voltage
time = df["# Seconds"]
voltage = df["DAQ1/ai1"].astype(float)

# Known Capacitance value
C = 0.017418 #Farads approx 18k microfarad

# Convert voltage ->
charge = voltage * C

# Combine into new DataFrame
out = pd.DataFrame({
    "# Seconds": time,
    "Charge (C)": charge
})

# Extract columns
#time = df["# Seconds"]
#charge = df["Charge (C)"]   # or whatever your current column is named

# Plot
plt.figure(figsize=(10,5))
plt.plot(time, charge, label="Charge vs Time", color="blue")

plt.xlabel("Time (s)")
plt.ylabel("Charge (C)")
plt.title("Charge vs Time")
plt.grid(True)
plt.legend()

plt.show()
# Save
"""
CHANGE CSV NAME TO BULB TYPE AND BULB #
"""

out.to_csv("Capacitor_Charge_Voltage_Output_10V_18Kmicrofarad_cap_6.3V_Bulb1_10milihentry_inductor.csv", index=False)

print(out)