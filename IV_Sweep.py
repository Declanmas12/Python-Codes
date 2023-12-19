from pymeasure.instruments.keithley import Keithley2450
import os
from datetime import datetime
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
 
#Connect to the instrument
keithley = Keithley2450("USB0::0x05E6::0x2460::04516939::INSTR")  # Change the address accordingly
 
def ivsweep(Volts):
    keithley.reset() # Reset the instrument to default settings
    keithley.use_front_terminals() # Sets the output to the front terminals
    keithley.apply_voltage() # Set source function to voltage
    keithley.compliance_current = 1 # current value before error occurs
    keithley.source_voltage = {Volts} # Set source voltage to 1.0V
    keithley.enable_source() # Turn on the output
 
    # You can now read the current using the following command
    current = keithley.measure_current(auto_range=True)
 
    print(f"Measured current: {current} mA")
    ivsweep_list_x.append(Volts)
    ivsweep_list_y.append(float(current))
 
 
#-------------------------------------------------------------------------
ivsweep_list_x = []
ivsweep_list_y = []
 
for mv in np.arange (1, -0.5, -0.005):
    ivsweep(mv)

plt.plot(ivsweep_list_x, ivsweep_list_y, label='Voltage Sweep Test')

plt.xlabel('mV')
plt.ylabel('mA')
plt.title('IV Sweep')
plt.legend()
 
# To display the plot
plt.show()
 
# To save the plot to a file (as a PNG image)
plt.savefig('sine_function_plot.png')