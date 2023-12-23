# Dr. D.Hughes 14/12/2023
# MicroLink Devices UK LTD
### Python code to measure the current and voltage across a thermoelectric sample ###

### Libraries To Import ###
from pymeasure.instruments.keithley import Keithley2450
import os
from datetime import datetime
from time import sleep
import numpy as np
import matplotlib.pyplot as plt

### Keithley Port Address ###
keithley = Keithley2450("GPIB::16")

### Current and Voltage Measurements ###
if keithley.id == "KEITHLEY INSTRUMENTS,MODEL 2450,04365704,1.6.4c": # ID of the Keithley system
    keithley.reset()
    keithley.beep(5E2, 1) # Beep to confirm connection (Hz, seconds)
    keithley.use_front_terminals() # Sets output to the front terminals

    ### Measurement Lists ###
    voltage=[]
    current=[]
    count=[]
    power=[]

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

        power.append((keithley.voltage * keithley.current)/4)

        sleep(1) # system rests before running again (seconds)

    keithley.shutdown()

    ### Graph Plotting ###
    figure, ax1 = plt.subplots(figsize=(8,8))
    ax2 = ax1.twinx()
    ax1.plot(count, current)
    ax2.plot(count, voltage)
    ax1.set_xlabel("Counts")
    ax1.set_ylabel("Current (A)")
    ax2.set_xlabel("Counts")
    ax2.set_ylabel("Voltage (V)")
    plt.title("Current & Voltage - " + current_date + " - "+ current_time)
    plt.legend()
    plt.show()
    plt.savefig("Current & Voltage - " +file_time+".png")

    ### Data Analysis and Sorting ###
    avg_V = str(np.average(voltage))
    err_V = str(np.std(voltage))
    avg_C = str(np.average(current))
    err_C = str(np.std(current))
    avg_pow = str(np.average(power))
    err_pow = str(np.std(power))
    Results = [count, voltage, current, power]

    ### Save Results to txt File ###
    with open("Thermoeletric_Results_"+ file_time +".txt", "w") as file: # file name and type
        file.write(current_date +"\t" + current_time)
        file.write("\n")
        file.write("Count (#) \t Voltage (V) \t Current (A) \t Power (W) \n")
        for x in zip(*Results):
            file.write("{0}\t{1}\t{2}\t{3}\n".format(*x))
        file.write("\n Average: \t "+ avg_V +"\t"+ avg_C +"\t"+ avg_pow)
        file.write("\n Error: \t "+ err_V +"\t"+ err_C +"\t"+ err_pow)
        file.close()

### Error Message ###
else:
    print("No Connection Found! Check The Connection and Port Address Number")