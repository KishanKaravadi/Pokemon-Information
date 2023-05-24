import PySimpleGUI as sg

# Define the initial layout with a column
layout = [
    [sg.Column([[sg.Text("Initial Text", key="-TEXT-")]], key="-COLUMN-")],
    [sg.Button("Update", key="-UPDATE-")],
    [sg.Button("Exit")]
]

window = sg.Window("Update Column Example", layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Exit":
        break
    elif event == "-UPDATE-":
        updated_text = "Updated Text"
        updated_column = [[sg.Text(updated_text, key="-TEXT-")]]
        window["-COLUMN-"].update(updated_column)

window.close()
