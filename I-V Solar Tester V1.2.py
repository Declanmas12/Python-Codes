# Dr. Declan Hughes 2023
# MicroLink Devices UK LTD
### Python code to measure the IV curve of a solar cell and output cell parameters ###

# UI and functionality imports
from pymeasure.instruments.keithley import Keithley2450
import PySimpleGUI as sg
import os
from datetime import datetime
from time import sleep
import numpy as np
import math as ma

# Plotting Imports
from matplotlib.ticker import NullFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

# IV Sweep Function
def ivsweep(Volts):
    keithley.reset() # Reset the instrument to default settings
    keithley.use_front_terminals() # Sets the output to the front terminals
    keithley.apply_voltage() # Set source function to voltage
    keithley.compliance_current = 1 # current value before error occurs
    keithley.source_voltage = Volts # Set source voltage to 1.0V
    keithley.enable_source() # Turn on the output

#Plotting Function
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

# List for looking at previous scans
x_total = []
y_total = []

# UI Theme
sg.theme('TealMono')

# Table Design
toprow=['', 'Date', 'Cell ID', 'PCE (%)', 'Voc (V)', 'Jsc (A/cm2)', 'Fill Factor (%)', 'Isc (A)', 'Pmax (W)']
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

# UI Layout and Design
tab1_layout = [[sg.Push(), sg.Text("Solar Simulator IV Sweep V2.0"), sg.Push()],
[sg.Text('Cell ID', size=(5, 1)), sg.InputText(key='-ID-'), sg.Text('Cell Area (cm2)', size=(12, 1)), sg.InputText(key='-Size-')],
[tbl1, sg.Canvas(key='-Graph-')],
[sg.Button("Clear Table"), sg.Push(), sg.Button("Save PNG"), sg.Button("Save JPEG")],
[sg.Input(expand_x=True, key='-FILE-'), sg.Button('SaveAs'), sg.Button('Save Table')], 
[sg.Button("Run"),sg.Button("Exit")],
[sg.Push(), sg.Text("MicroLink Devices UK LTD 2023"), sg.Push()]]

tab2_layout = [[sg.Push(), sg.Radio("AM1.5G", "Sun In", default=True), sg.Radio("AM0", "Sun In", default=False), sg.Push()], 
[sg.Push(), sg.Text('Start Voltage (V)', size=(15, 1)), sg.InputText("1.2", key='-Sv-'), sg.Text('End Voltage (V)', size=(15, 1)), sg.InputText("-0.5", key='-Ev-'), sg.Text('Voltage Steps (V)', size=(15, 1)), sg.InputText("0.005", key='-Step-'), sg.Push()]]

layout = [[sg.TabGroup([[sg.Tab('I-V Scan', tab1_layout), sg.Tab('Settings', tab2_layout)]])]]

# Create the window
window = sg.Window("MLDUK - IV Tester", layout, resizable=True, finalize=True)

# Draw the plot area
fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
fig_canvas_agg = draw_figure(window['-Graph-'].TKCanvas, fig)

# Row Number
Num=0

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
            keithley = Keithley2450("USB0::0x05E6::0x2460::04516939::INSTR")
        except:
            sg.popup("Keithley Not Connected!")
            continue

        ### Current and Voltage Measurements ###
        try:
            if keithley.id == "KEITHLEY INSTRUMENTS,MODEL 2460,04516939,1.7.7b": # ID of the Keithley system
                keithley.reset()
                keithley.beep(5E2, 1) # Beep to confirm connection (Hz, seconds)
                keithley.use_front_terminals() # Sets output to the front terminals

                # Time of scan for file
                file_time = now.strftime("%H_%M_%S")
                file_date = now.strftime("%d-%m-%Y")

                ### Measurement Lists ###
                voltage=[]
                current=[]
                jsc = []
                power=[]

                # Sun Intensity using UI
                if event == "AM1.5G":
                    Sun_Intensity = 100
                if event == "AM0":
                    Sun_Intensity = 136.7

                # Step Size Sign Correction
                if float(values['-Sv-']) < float(values['-Ev-']):
                    Steps = -float(values['-Step-'])
                else:
                    Steps = float(values-'-Step-')

                # I-V Sweep (Step size is now automatically calculated in the right direction)
                try:
                    for mv in np.arange(float(values['-Sv-']), float(values['-Ev-']), Steps):
                        ivsweep(mv)
                        voltage.append(keithley.voltage)
                        current.append(keithley.current)
                        jsc.append(keithley.current/float(values['-Size-']))
                        power.append(float(keithley.voltage * (keithley.current)/float(values['-Size-'])))
                        fig.plot(voltage, current) # Creates the graph
                        window.Refresh() # Draw graph in real time

                # Look at previous scans
                    x_total.append(voltage)
                    y_total.append(current)

                except:
                    if values['-Sv-'] == str():
                        sg.popup("Please enter starting voltage")
                    if values['-Ev-'] == str():
                        sg.popup("Please enter ending voltage")
                    if values['-Size-'] == str():
                        sg.popup("Please enter cell area")

                #Maximum power, voltage, current, and fill factor
                pmax = float(max(power))
                vmax = float(voltage[power.index(max(power))])
                jmax = float(jsc[power.index(max(power))])
                voc = float(voltage[current.index(ma.isclose(0, rel_tol=1e-5))])
                isc = float(current[voltage.index(ma.isclose(0, rel_tol=1e-5))])
                jsc = float(current[voltage.index(ma.isclose(0, rel_tol=1e-5))]/float(values['-Size-']))
                FF = float((pmax/(jsc*voc))*100)
                Pin = float(Sun_Intensity*float(values['-Size-'])) #AM1.5G 100 mW/cm2
                pce = float((voc*isc*FF)/Pin)

                # Adds value to the table rows
                rows.append([str(Num),
                current_date, 
                str(values['-ID-']),
                str(pce),
                str(voc), 
                str(isc), 
                str(jsc),
                str(FF),
                str(pmax)])

                Num += 1

                ### Create folder and save IV curves to txt File ###
                Results = [voltage, current, jsc]

                if not os.path.exists('./'+file_date):
                    os.mkdir('./'+file_date)
                    os.chdir('./'+file_date)
                    with open(file_date + file_time + values['-ID-'] + ".txt", "w") as file: # file name and type
                        file.write(current_date +"\t" + current_time)
                        file.write("\n")
                        file.write(values['-ID-'])
                        file.write("\n")
                        file.write("Voltage (V) \t Current (A) \t Current Density (A/cm2) \n")
                        for x in zip(*Results):
                            file.write("{0}\t{1}\t{2}\n".format(*x))
                        file.close()
                else:
                    os.chdir('./'+file_date)
                    with open('./'+file_date + file_time + values['-ID-'] + ".txt", "w") as file: # file name and type
                        file.write(current_date +"\t" + current_time)
                        file.write("\n")
                        file.write(values['-ID-'])
                        file.write("\n")
                        file.write("Voltage (V) \t Current (A) \t Current Density (A/cm2) \n")
                        for x in zip(*Results):
                            file.write("{0}\t{1}\t{2}\n".format(*x))
                        file.close()

                # Updates table rows
                tbl1.update(values=rows)

                # Refreshes the table window
                window.refresh()

                keithley.shutdown()

        ### Error Message ###
        except:
            sg.popup("Wrong Keithley Model Used! Please check the right model is called in the code")
            continue

        # Saving the table as a CSV
    elif event == 'SaveAs':
        filename = values['-FILE-']
        filename = sg.popup_get_file("Save As", default_extension='.csv', default_path=filename, save_as=True, file_types=(("All CSV Files", "*.csv"),), no_window=True)
        if filename:
            window['-FILE-'].update(filename)

    elif event == 'Save Table':
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


    if '+CLICKED+' in event:
        try:
            fig.clf()
            fig.plot(x_total[int(toprow[0])], y_total[int(toprow[0])])
            window.Refesh()
        except:
            sg.popup("No Data Currently In The Table")
            continue
      
    if event == "Save PNG":
        fig.savefig(values['-ID-']+file_time+'.png')

    if event == "Save JPEG":
        fig.savefig(values['-ID-']+ '-' +file_time+'.jpeg')

     # Clears table on button press
    if event == "Clear Table":
        rows=[]
        tbl1.update(values=rows)

    # End program if user closes window or presses exir
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()