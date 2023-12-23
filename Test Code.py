from pymeasure.instruments import list_resources
import PySimpleGUI as sg

resources = list_resources()

names = []

for x in range(0, len(resources),1):
    names.append(resources[x])

lst1 = sg.Combo(names, font=('Arial Bold', 14),  expand_x=True, enable_events=True,  readonly=False, key='-COMBO-')
lst2 = sg.Combo(names, font=('Arial Bold', 14),  expand_x=True, enable_events=True,  readonly=False, key='-COMBO-')

layout = [[lst1],
          [lst2]]

window = sg.Window('Combobox Example', layout, size=(715, 200))

while True:
    event, values = window.read()

    # End program if user closes window or presses exit
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()