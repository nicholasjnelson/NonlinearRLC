import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import scipy.optimize as spo

# Tell Matplotlib to ignore the >20 figures open warning
plt.rcParams.update({'figure.max_open_warning': 0}) 

# --- Configuration ---
folder_path = r"E:\Summer Research\2026_06_02 Voltage_Current 6.3V .15A" 
area = 1e-5
sigma = 5.67e-8  

def analyze_folder(folder_path, area):
    folder = Path(folder_path)
    
    if not folder.is_dir():
        print(f"Error: The directory '{folder_path}' does not exist.")
        return

    fit_results = []
    print(f"Scanning folder: {folder_path}...")
    
    for file_path in folder.glob("*.txt"):
        try:
            df = pd.read_csv(file_path)
            V = df['Voltage (V)'].values
            I = df['Current (A)'].values
            
            valid_indices = I > 0
            V = V[valid_indices]
            I = I[valid_indices]
            
            if len(I) == 0:
                print(f"Skipping {file_path.name}: No valid current data > 0.")
                continue

            R = V / I
            P = V * I
            T = (P / (sigma * area)) ** 0.25
            x_axis = (area**0.25) * T
            lin_func = lambda x, m, b: m*x+b
            params, p_cov = spo.curve_fit(lin_func, x_axis, R)
            print(params)
            
            plt.figure(figsize=(10, 8))
            plt.plot(x_axis, R, marker='o', linestyle='', color='teal', label='Data Points')
            plt.plot(x_axis, lin_func(x_axis, params[0], params[1])) 
            
            plt.title(f'Resistance vs. $A^{{0.25}} \cdot T$ \n({file_path.name})')
            plt.xlabel('$A^{0.25} \cdot T$ ($m^{0.5} \cdot K$)')
            plt.ylabel('Resistance ($\Omega$)')
            plt.grid(True)
            plt.legend()
            
            # Show the plot, but do NOT close it!
            plt.show() 
            print(f"Generated plot for: {file_path.name}")

        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")

    if fit_results:
        summary_df = pd.DataFrame(fit_results)
        print("\n" + "="*60)
        print("Processing Complete. Line of Best Fit Summary:")
        print("="*60)
        print(summary_df.to_string(index=False))
        
        summary_csv_path = folder / "linear_fit_summary.csv"
        summary_df.to_csv(summary_csv_path, index=False)
    else:
        print("No valid files were processed.")

if __name__ == "__main__":
    analyze_folder(folder_path, area)