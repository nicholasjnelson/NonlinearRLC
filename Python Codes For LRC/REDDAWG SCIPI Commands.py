import pyvisa


#need to make a resource manager to automate
rm = pyvisa.ResourceManager()
#list RM resources to find USB ID for each automated system (for this should be 2, DMM and PS)

rm.list_resources()
print(rm.list_resources())

RDP_FG2A = rm.open_resource('ASRL7::INSTR')

scope = rm.open_resource('USB0::0x0699::0x03A3::C020553::INSTR')


print(scope.query("*IDN?"))
#print(scope.query("*OPTIONS?"))
#(scope.query("SYST:HELP?"))
#print(scope.query("HELP:SYST?"))
#print(scope.query("SYST:CMD?"))
#print(scope.query("SYST:DESC?"))
#print(scope.query("SYST:HELP:KEYS?"))
#print(scope.query("HELP:CMDs?"))
#print(scope.query("SYST:ERR?"))
#zprint(scope.query("SYST:COMM?"))
#print(scope.query("*OP?"))
#print(options)

#error = RDP_FG2A.query("*SYST:ERR?")
#print(error)
print(RDP_FG2A.query("SYST:ERR?"))
#------------------------------------------------------------------------
idn = RDP_FG2A.query("*IDN?")
print(idn)

help_text = RDP_FG2A.query("HELP?")
print(help_text)
print(RDP_FG2A.query("*OPTIONS?"))
print(RDP_FG2A.query("SYST:HELP?"))
print(RDP_FG2A.query("HELP:SYST?"))
print(RDP_FG2A.query("SYST:CMD?"))
print(RDP_FG2A.query("SYST:DESC?"))
print(RDP_FG2A.query("SYST:HELP:KEYS?"))
print(RDP_FG2A.query("HELP:CMDs?"))
print(RDP_FG2A.query("SYST:ERR?"))
print(RDP_FG2A.query("SYST:COMM?"))
idn = RDP_FG2A.query("*IDN?")
print(RDP_FG2A.query("*OPTIONS?"))
#print(options)

#error = RDP_FG2A.query("*SYST:ERR?")
#print(error)
print(RDP_FG2A.query("SYST:ERR?"))
rm.close()

"""
Red Dog Physics SineDriver V3.3 - firmware ItsyBitsy_20260728

Red Dog Physics SineDriver V3.3 - firmware ItsyBitsy_20260728



Available Commands:

  *IDN? - Equipment and firmware ID

  *RST - Reset to default condition

  *TST - Test for centering adjustment (not yet implemented)

  *ESR - Report Error Status Register

  *CSR - Clear error Status Register

  FREQ ?|(value) - request (?) or set (value) frequency

  COIL ?|(0|1) - request coil-drive status (?) or set coil on (1) or off (0)

  AMPL ?|(value) - request (?) or set (value) amplitude, 0-1000
  
  ZERO - define current position as zero
"""