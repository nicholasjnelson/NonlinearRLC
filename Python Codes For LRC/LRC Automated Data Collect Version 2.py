# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 10:28:34 2026

@author: AnthonySB2
"""

import time 
import pyvisa 
import nidaqmx
import numpy as np
import matplotlib.pyplot as plot 
import matplotlib.ticker as ticker

rm = pyvisa.ResourceManager()
print("Available VISA resources:", rm.list_resources())

#Red DAWG Physics FG2A V3.2 High-Current Generator Beginning Parameters
RDP_FG2A = rm.open_resource('ASRL7::INSTR')
idn = RDP_FG2A.query("*IDN?")
print(idn)

RDP_FG2A.write("COIL0")
print("RED DAWG OUTPUT SET:", RDP_FG2A.query("COIL?"))

RDP_FG2A.write("FREQ00")
print("Frequency:", RDP_FG2A.query("FREQ?"),"Hz")

RDP_FG2A.write("AMPL000")
print("Voltage Amplitude", RDP_FG2A.query("AMPL?"), "Milivolts")

RDP_FG2A.write("ZERO")

print("RED DAWG OUTPUT SET:", RDP_FG2A.query("COIL?"))
rm.close()

#-----------------------------------------------------------------------------

from nidaqmx.constants import READ_ALL_AVAILABLE, AcquisitionType

#------------------------------------------------------------------------------

def start_up_RDP_FG2A():
    rm = pyvisa.ResourceManager()
    
    RDP_FG2A = rm.open_resource('ASRL7::INSTR')
    RDP_FG2A.write("COIL0")
    print("RED DAWG OUTPUT SET:", RDP_FG2A.query("COIL?"))
    RDP_FG2A.write("FREQ10")
    print("Frequency:", RDP_FG2A.query("FREQ?"),"Hz")
    RDP_FG2A.write("AMPL1000")
    print("Voltage Amplitude", RDP_FG2A.query("AMPL?"), "milivolts")
    RDP_FG2A.write("ZERO")
    
    print("RDP_FG2A configured")
    return rm, RDP_FG2A

#------------------------------------------------------------------------------

def estimate_frequency(signal, dt):
    """
    Estimate the dominant frequency of a waveform using FFT.
    signal: numpy array of samples
    dt: sample interval (seconds)
    """
    N = len(signal)

    # FFT
    fft_vals = np.fft.rfft(signal)
    fft_freqs = np.fft.rfftfreq(N, dt)

    # Magnitude spectrum
    mag = np.abs(fft_vals)

    # Peak frequency (ignore DC at index 0)
    peak_index = np.argmax(mag[1:]) + 1
    peak_freq = fft_freqs[peak_index]

    return peak_freq

#------------------------------------------------------------------------------

def run_daq_acquisition():
    print("DAQ acquisition started...")
    
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan(
            "DAQ1/ai0",
            min_val=-0.5,
            max_val=0.5,
            terminal_config=nidaqmx.constants.TerminalConfiguration.DIFF)

        task.ai_channels.add_ai_voltage_chan(
            "DAQ1/ai1",
            min_val=-0.5,
            max_val=0.5,
            terminal_config=nidaqmx.constants.TerminalConfiguration.DIFF)

        task.ai_channels.add_ai_voltage_chan(
            "DAQ1/ai2",
            min_val=-10.0,
            max_val=10.0,
            terminal_config=nidaqmx.constants.TerminalConfiguration.DIFF)

        task.timing.cfg_samp_clk_timing(
            1000.0,
            sample_mode=AcquisitionType.FINITE,
            samps_per_chan=2000
        )
        
        waveforms = task.read_waveform(READ_ALL_AVAILABLE)
        if not isinstance(waveforms, list):
            waveforms = [waveforms]
            
        min_start_time = min(w.timing.start_time for w in waveforms)
        num_channels = len(waveforms)
        
        fig, axes = plot.subplots(num_channels, 1, figsize=(10,6), sharex=True)
        if num_channels == 1:
            axes = [axes]
        
        
        # Corrected loop with sanity checks + correct time vector 
        # ---------------------------------------------------------------------
        for ax, w in zip(axes, waveforms): 
    
            # --- Sanity checks ---
            dt = w.timing.sample_interval.total_seconds()
            expected_duration = dt * (w.sample_count - 1)
            your_duration = dt * w.sample_count

            print(f"\nChannel {w.channel_name}")
            print(f"Sample count: {w.sample_count}")
            print(f"Sample interval dt: {dt}")
            print(f"Expected duration: {expected_duration}")
            print(f"Your old duration: {your_duration}")

            # --- Correct uniform time vector ---
            time_offset = (w.timing.start_time - min_start_time).total_seconds()
            time_data = time_offset + np.arange(w.sample_count) * dt

            # --- Plot ---
            ax.plot(time_data, w.scaled_data)
            ax.set_ylabel(w.units)
            ax.set_title(f"Channel {w.channel_name}")
            ax.grid(True)
            ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.4f'))

            # --- Frequency estimation ---
            freq_est = estimate_frequency(w.scaled_data, dt)
            print(f"Estimated frequency for {w.channel_name}: {freq_est:.4f} Hz")
        
        axes[-1].set_xlabel("Seconds")
        fig.tight_layout()
        plot.show()
        
        # CSV Export
        sample_interval = waveforms[0].timing.sample_interval.total_seconds()
        sample_count = waveforms[0].sample_count
        time_data = np.arange(sample_count) * sample_interval
        
        voltage_matrix = np.column_stack([wf.scaled_data for wf in waveforms])
        data_to_save = np.column_stack((time_data, voltage_matrix))
        
        header = "Seconds," + ",".join([wf.channel_name for wf in waveforms])
        np.savetxt(
            "daq_output_multichannel_6.3V_0.15ARated_Bulb1.csv",
            data_to_save,
            delimiter=",",
            fmt="%.6f",
            header=header
        )
    
    print("DAQ acquisition complete.")

#--------------------------------------------------------------------------------------------   

if __name__ == "__main__":
    start = input("Start experiment? (Y/N):").strip().lower()
   
    if start != "y":
        print("Experiment aborted.")
    else:
        rm, RDP_FG2A = start_up_RDP_FG2A()
        print("Turning on Red DAWG Function Generator...")
        RDP_FG2A.write("COIL1")
        time.sleep(5.0)
        
        run_daq_acquisition()
        
        print("Turning off Red DAWG Function Generator...")
        RDP_FG2A.write("COIL0")
        print("RDP_FG2A output:", RDP_FG2A.query("COIL?"))
        
        rm.close()
        print("Experiment complete.")