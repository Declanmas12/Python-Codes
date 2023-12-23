from pymeasure.instruments.keithley import Keithley2450
import os
from datetime import datetime
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


### Get Date and Time ###
now = datetime.now()
current_date = now.strftime("%d/%m/%Y")
current_time = now.strftime("%H:%M:%S")
file_time = now.strftime("%H_%M_%S")
 
### Connect to the instrument ###
keithley = Keithley2450("USB0::0x05E6::0x2460::04516939::INSTR")  # Change the address accordingly
 
def ivsweep(Volts):
    keithley.reset() # Reset the instrument to default settings
    keithley.use_front_terminals() # Sets the output to the front terminals
    keithley.apply_voltage() # Set source function to voltage
    keithley.compliance_current = 1 # current value before error occurs
    keithley.source_voltage = Volts # Set source voltage to 1.0V
    keithley.enable_source() # Turn on the output
 
    # You can now read the current using the following command
    keithley.measure_current(auto_range=True)

    ivsweep_list_x.append(Volts)
    ivsweep_list_y.append(keithley.current)
 
#-------------------------------------------------------------------------

if keithley.id == "KEITHLEY INSTRUMENTS,MODEL 2460,04516939,1.7.7b":

    ivsweep_list_x = []
    ivsweep_list_y = []

    now = datetime.now()
    current_date = now.strftime("%d/%m/%Y")
    current_time = now.strftime("%H:%M:%S")
    file_time = now.strftime("%H_%M_%S")

    for mv in np.arange (1.2, -0.5, -0.005):
        ivsweep(mv)

else:
    print("Error! Check Connection and Port Address")

plt.plot(ivsweep_list_x, ivsweep_list_y, label='I-V Curve')

plt.xlabel('V')
plt.ylabel('mA')
plt.title("I-V Curve - " + file_time)
plt.xlim(0,1)
plt.legend()
 
### To display the plot ###
plt.show()

### To save the plot to a file (as a PNG image) ###
plt.savefig("IV Curve_"+file_time+".png")