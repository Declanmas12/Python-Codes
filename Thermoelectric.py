#Dr. D.Hughes 14/12/2023
#Python code to measure the current and voltage across a thermoelectric sample

### Libraries To Import ###
from pymeasure.instruments.keithley import Keithley2450
import os
from datetime import datetime
from time import sleep
import numpy as np

### Keithley Port Address ###
keithley = Keithley2450("USB0::0x05E6::0x2460::04516939::INSTR")

### Current and Voltage Measurements ###
if keithley.id == "KEITHLEY INSTRUMENTS,MODEL 2460,04516939,1.7.7b": # ID of the Keithley system
    keithley.reset()
    keithley.beep(5E2,1) # Beep to confirm connection (Hz, seconds)
    keithley.use_front_terminals() # Sets output to the front terminals

    ### Measurement Lists ###
    voltage=[]
    current=[]
    count=[]

    ### Time and Date ###
    now = datetime.now()
    current_date = now.strftime("%d/%m/%Y")
    current_time = now.strftime("%H:%M:%S")
    file_time = now.strftime("%H_%M_%S")


    for i in range(0,10,1): # How many meaurements made in 1 run (start, finish, step). All numbers must be integers

        count.append(i)

        keithley.apply_current() # set-up source 
        keithley.compliance_voltage = 1 # Max voltage value before error
        keithley.source_current = 0 # applied current value
        keithley.enable_source() # applies source
        keithley.measure_voltage(auto_range=True) # measures the voltage
        voltage.append(keithley.voltage) # adds voltage value to list

        keithley.apply_voltage()
        keithley.compliance_current = 1
        keithley.source_voltage = 0
        keithley.enable_source()
        keithley.measure_current(auto_range=True)
        current.append(keithley.current)

        sleep(1) # system rests before running again (seconds)

    keithley.shutdown()

    Results = [count, voltage, current]

    ### Save Results to txt File ###
    with open("Thermoeletric_Results_"+ file_time +".txt", "w") as file: # file name and type
        file.write(current_date +"\t" + current_time)
        file.write("\n")
        file.write("Count (#) \t Voltage (V) \t Current (A) \n")
        for x in zip(*Results):
            file.write("{0}\t{1}\t{2}\n".format(*x))
        file.close()

### Error Message ###
else:
    print("No Connection Found! Check The Connection and Port Address Number")