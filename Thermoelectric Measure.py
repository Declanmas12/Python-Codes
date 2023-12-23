# Dr. Declan Hughes & Dr. Geraint Howells 2023
# Swansea University - Engineering
### Python code to measure the current and voltage across a thermoelectric sample ###

import PySimpleGUI as sg
from pymeasure.instruments.keithley import Keithley2450
import os
from datetime import datetime
from time import sleep
import numpy as np
import matplotlib.pyplot as plt

sg.theme('Topanga')

toprow=['Date', 'Time','Voltage (V)', 'Current (A)', 'Power (W)']
rows=[]

tbl1 = sg.Table(values=rows, headings=toprow,
   auto_size_columns=True,
   display_row_numbers=False,
   justification='center', key='-TABLE-',
   selected_row_colors='red on yellow',
   enable_events=True,
   expand_x=True,
   expand_y=True,
 enable_click_events=True)

tab1_layout = [[sg.Push(), sg.Text("Thermoelectric Measurement V1"), sg.Push()],
[tbl1],
[sg.Button("Clear Table")],
[sg.Input(expand_x=True, key='-FILE-'), sg.Button('SaveAs'), sg.Button('Save Table')], 
[sg.Button("Run"),sg.Button("Exit")],
[sg.Push(), sg.Text("Dr. Declan Hughes & Dr. Geraint Howells 2023"), sg.Push()]]

tab2_layout = [[sg.Push(), sg.Text('Maximum Voltage (V)', size=(20, 1)), sg.InputText("1", key='-Mv-'), sg.Text('Maximum Current (A)', size=(20, 1)), sg.InputText("1", key='-Mc-'), sg.Push()], 
[sg.Push(), sg.Text('Number of Scans', size=(20, 1)), sg.InputText("1", key='-No-'), sg.Text('Time Between Scans (s)', size=(20, 1)), sg.InputText("1", key='-Time-'), sg.Push()]]

layout = [[sg.TabGroup([[sg.Tab('Measurements', tab1_layout), sg.Tab('Settings', tab2_layout)]])]]

# Create the window
window = sg.Window("DH-Thermoelectric", layout, resizable=True)

# Create an event loop
while True:
    event, values = window.read()

    ### Time and Date ###
    now = datetime.now()
    current_date = now.strftime("%d/%m/%Y")
    current_time = now.strftime("%H:%M:%S")
    file_time = now.strftime("%H_%M_%S")

    if event == "Run":
        ### Keithley Port Address ###
        try:
            keithley = Keithley2450("GPIB::16")
        except:
            sg.popup("Keithley Not Connected")
            continue

        ### Current and Voltage Measurements ###
        try:
            if keithley.id == "KEITHLEY INSTRUMENTS,MODEL 2450,04365704,1.6.4c": # ID of the Keithley system
                keithley.reset()
                keithley.beep(5E2, 1) # Beep to confirm connection (Hz, seconds)
                keithley.use_front_terminals() # Sets output to the front terminals

                try:
                    for i in range(0,int(values['-No-'])): # How many meaurements made in 1 run (start, finish, step). All numbers must be integers

                        now = datetime.now()
                        current_date = now.strftime("%d/%m/%Y")
                        current_time = now.strftime("%H:%M:%S")

                        keithley.apply_current() # set-up source 
                        keithley.compliance_voltage = values['-Mv-'] # Max voltage value before error
                        keithley.source_current = 0 # applied current value
                        keithley.enable_source() # applies source
                        keithley.measure_voltage(auto_range=True) # measures the voltage

                        keithley.apply_voltage()
                        keithley.compliance_current = values['-Mc-']
                        keithley.source_voltage = 0
                        keithley.enable_source()
                        keithley.measure_current(auto_range=True)

                        rows.append([current_date, current_time, str(keithley.voltage), str(keithley.current), str((keithley.voltage * keithley.current)/4)])
                        
                        tbl1.update(values=rows)
                        window.refresh()

                        sleep(float(values['-Time-'])) # system rests before running again (seconds)

                    keithley.shutdown()
                except:
                    if values['-No-'] == str():
                        sg.popup("Need to give scan number")
                    if values['-Time-'] == str() and int(values['-No-']) > 1:
                        sg.popup("Need to give time between scans (can be 0)")
                    if values['-Mv-'] == str():
                        sg.popup("Need to give maximum voltage value")
                    if values['-Mc-'] == str():
                        sg.popup("Need to give maximum current value")
        except:
            print("Wrong Keithley Address")
            continue

        ### Error Message ###
        else:
            print("No Connection Found! Check The Connection and Port Address Number")

    # End program if user closes window or presses exit
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    
    # Clears table on button press
    if event == "Clear Table":
        rows=[]
        tbl1.update(values=rows)

    # Saving the table as a CSV
    elif event == 'SaveAs':
        filename = values['-FILE-']
        filename = sg.popup_get_file("Save As", default_extension='.csv', default_path=filename, save_as=True, file_types=(("All CSV Files", "*.csv"),), no_window=True)
        if filename:
            window['-FILE-'].update(filename)

    elif event == 'Save':
        filename = values['-FILE-']
        if filename:
            try:
                with open(filename, 'wt') as f:
                    f.write('\n'.join([','.join(item) for item in [toprow]+rows]))
                sg.popup(f"File {repr(filename)} Saved!")
                continue
            except PermissionError:
                pass
        sg.popup(f"Cannot open file {repr(filename)}!")


window.close()