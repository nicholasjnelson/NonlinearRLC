# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 13:44:07 2026

@author: AnthonySB2
"""

import pandas as pd
import matplotlib.pyplot as plt
# Load CSV
df = pd.read_csv("E:/6.3V .15A LRC Trial/daq_output_multichannel_6.3V_0.15ARated_Bulb1.csv")

# Extract time + voltage
time = df["# Seconds"]
voltage = df["DAQ1/ai0"].astype(float)

# Known resistance value
R = 0.1

# Convert voltage → current
current = voltage / R

# Combine into new DataFrame
out = pd.DataFrame({
    "# Seconds": time,
    "Current (A)": current
})

# Extract columns
#time = df["# Seconds"]
#current = df["Current (A)"]   # or whatever your current column is named

# Plot
plt.figure(figsize=(10,5))
plt.plot(time, current, label="Current vs Time", color="blue")

plt.xlabel("Time (s)")
plt.ylabel("Current (A)")
plt.title("Current vs Time")
plt.grid(True)
plt.legend()

plt.show()
# Save
"""
CHANGE CSV NAME TO BULB TYPE AND BULB #
"""
out.to_csv("current_output_shunt_6.3V_Bulb8.csv", index=False)

print(out)