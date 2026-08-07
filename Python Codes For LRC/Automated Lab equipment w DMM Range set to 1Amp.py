import pyvisa
import time
import csv

#need to make a resource manager to automate
rm = pyvisa.ResourceManager()
#list RM resources to find USB ID for each automated system (for this should be 2, DMM and PS)

rm.list_resources()
print(rm.list_resources())

#rm.list_resoource('ASRL5::INSTR')
dmm = rm.open_resource('USB0::0x05E6::0x2100::1310875::INSTR')
supply = rm.open_resource('ASRL5::INSTR')




#set up the power supply
#supply.write('BEEP1')
supply.write('VSET1:0.00')
supply.write('ISET1:0.3')
supply.write('OUT1')
#set DMM to current mode in dc "I (amps)"

dmm.write('FUNCTION "CURRent:DC"')
dmm.write('CURRent:DC:RANGE:AUTO OFF')
dmm.write('CURRent:DC:RANGE 1')

print(dmm.query("CURRent:DC:RANGE?"))
print(dmm.query("CURRent:DC:RANGE:AUTO?"))

#Data collecting
start_voltage = 0.00 #volts
stop_voltage = 3.9 #volts
step_voltage = 0.10 #volts
settling_time = 0.5 #time seconds



with open("voltage_current_log_3.8V_0.3A.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Voltage (V)", "Current (A)"])
   
    voltage = start_voltage
    while voltage <= stop_voltage:
        #set voltage
        supply.write(f"VSET1:{voltage:.2f}")
        time.sleep(settling_time)
       
        #measure current
        current = float(dmm.query(":READ?"))
       
        #save to CSV
        writer.writerow([f"{voltage:.2f}", current])
        print(f"V={voltage:.2f} V, I={current:.6f} A")
       
        voltage += step_voltage
       
    #turn off after operation
    supply.write('BEEP')
    supply.write('OUT0')
    
    #close connections
    supply.close()
    dmm.close()
    rm.close()
  
    

