import PySimpleGUI as sg

from matplotlib.ticker import NullFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

from time import sleep
from datetime import datetime
import random as rnd
import os

sg.theme('Topanga')

toprow=['Date', 'Time','Voltage (V)', 'Current (A)', 'Power (W)']
rows=[]

tbl1 = sg.Table(values=rows, headings=toprow,
   auto_size_columns=True,
   display_row_numbers=False,
   justification='center', key='-TABLE-',
   selected_row_colors='red on yellow',
   select_mode=sg.TABLE_SELECT_MODE_BROWSE,
   enable_events=True,
   expand_x=True,
   expand_y=True,
 enable_click_events=True)

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

tab1_layout = [[sg.Push(), sg.Text("Thermoelectric Measurement V1"), sg.Push()],
[sg.Push(), sg.Text('Maximum Voltage (V)', size=(20, 1)), sg.InputText("1",key='-Mv-'), sg.Text('Maximum Current (A)', size=(20, 1)), sg.InputText(key='-Mc-'), sg.Push()], 
[sg.Push(), sg.Text('Number of Scans', size=(20, 1)), sg.InputText("1", key='-No-'), sg.Text('Time Between Scans (s)', size=(20, 1)), sg.InputText(key='-Time-'), sg.Push()],
[tbl1, sg.Canvas(key='-Graph-')],
[sg.Button("Clear Table")],
[sg.Input(expand_x=True, key='-FILE-'), sg.Button('SaveAs'), sg.Button('Save Table')],
[sg.Button("Run"),sg.Button("Exit")],
[sg.Push(), sg.Text("Dr. Declan Hughes & Dr. Geraint Howells 2023"), sg.Push()]]

tab2_layout = [[sg.T("Hello")]]

layout = [[sg.TabGroup([[sg.Tab('Tab 1', tab1_layout), sg.Tab('Tab 2', tab2_layout)]])]]

x=[]
y=[]
x_total = []
y_total=[]

# Create the window
window = sg.Window("DH-Thermoelectric", layout, resizable=True, finalize=True)

fig = matplotlib.figure.Figure(dpi=100)
fig.add_subplot(111)
fig_canvas_agg = draw_figure(window['-Graph-'].TKCanvas, fig)

# Create an event loop
while True:

    now = datetime.now()
    current_date = now.strftime("%d/%m/%Y")
    current_time = now.strftime("%H:%M:%S")
    file_time = now.strftime("%H_%M_%S")

    event, values = window.read()

    if event == "Run":
        try:

            for i in range(0,int(values['-No-']),1):

                fig_canvas_agg.get_tk_widget().forget()

                x1=rnd.randint(1,100)
                y1=rnd.randint(1,100)

                x.append(x1)
                y.append(y1)

                now = datetime.now()
                current_date = now.strftime("%d/%m/%Y")
                current_time = now.strftime("%H:%M:%S")

                rows.append([current_date, current_time, str(x1), str(y1), str(x1*y1)])
                tbl1.update(values=rows)

                fig = matplotlib.figure.Figure(dpi=100)
                fig.add_subplot(111).scatter(x,y)
                fig_canvas_agg = draw_figure(window['-Graph-'].TKCanvas, fig)
                window.refresh()

                sleep(float(values['-Time-']))

        except:
            if values['-No-'] == str():
                sg.popup("Need to give number of scans number")
            if values['-Time-'] == str() and int(values['-No-']) > 1:
                sg.popup("Need to give time between scans (can be 0)")

    if event == "Clear Table":
        rows=[]
        x=[]
        y=[]
        tbl1.update(values=rows)

    # End program if user closes window or presses exir
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if '+CLICKED+' in event:
        try:
            print("{}".format(event[2][0]))
        except:
            sg.popup("No Data Currently In The Table")
            continue
    
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
                sg.popup(f"File {repr(filename)} Saved !!!")
                continue
            except PermissionError:
                pass
        sg.popup(f"Cannot open file {repr(filename)} !!!")

window.close()