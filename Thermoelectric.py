#Dr. D.Hughes 14/12/2023
#Python code to measure the current and voltage across a thermoelectric sample

### Libraries To Import ###
from pymeasure.instruments.keithley import keithley2450
import os
from datetime import datetime
from time import sleep
import numpy as np

### Measurement Lists ###
voltage=[]
current=[]
count=[]

### Time and Date ###
now = datetime.now()
current_date = now.strftime("%d/%m/%Y")
current_time = now.strftime("%H:%M:%S")

### Keithley GPIB Address ###
keithley = keithley2450("GPIB::1")

### Current and Voltage Measurements ###
if keithley == keithley2450("GPIB::1"): #GPIB number must match above call
    keithley.beep(2E3,2) #Beep to confirm connection (Hz, seconds)
    keithley.reset()
    keithley.use_front_terminals()

    for i in range(0,10,1): #How many meaurements made in 1 run (start, finish, step). All numbers must be integers

        count.append(i)

        keithley.apply_current() #set-up source 
        keithley.compliance_voltage = 1 #Max voltage value before error
        keithley.source_current = 0 #applied current
        keithley.enable_source() #applies source
        keithley.measure_voltage(auto_range=True) #measures the voltage
        voltage.append(keithley.voltage) #adds voltage value to list

        keithley.apply_voltage()
        keithley.compliance_current = 1
        keithley.source_voltage = 0
        keithley.enable_source()
        keithley.measure_current(auto_range=True)
        current.append(keithley.current)

        sleep(1) #system rests before running again (seconds)

    keithley.shutdown()

    ### Save Results to txt File ###
    with open("Thermoeletric_Results"+current_time+".txt", "w") as file:
        file.write(current_date +"\t" + current_time)
        file.write("")
        file.write("Count (#) \t Voltage (V) \t Current (A)")
        for t in len(count):
            file.write(count[t] + "\t" + voltage[t] + "\t" + current [t])
        file.close()

    ### Print Results to Help Debug ###
    #print("Voltage (V) \t Current (A)")
    #for y in len(voltage):
        #print(voltage[y] + "\t" + current[y])

### Error Message ###
else:
    print("No GPIB Connection Found! Check the connection and GPIB address number")