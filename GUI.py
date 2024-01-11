import sys
import PySimpleGUI as sg
import threading


sg.theme("DarkAmber")

layout = [[sg.Text("FAME Master Sheet File Location:", font=('Times New Roman', 16)),
           sg.In(size=(25, 1), enable_events=True, key="-FILE-"),
           sg.FileBrowse()],[sg.Text('Enter Name of Output HTML:', font=('Times New Roman',16))],
          [sg.Input(do_not_clear=False)],
          [sg.Checkbox("Open in Python Browser?", key = 's1', font = ('Times New Roman',12), default = True)],
          [sg.Button("Execute Visualizer"), sg.Button("Close")],
          [sg.ProgressBar(max_value=10, orientation='h', size=(20, 20), key='progress')]
          ]

window = sg.Window("Quality Control Visualizer", layout, margins=(100, 100), element_justification='c')

#Element of the progress bar to make updating easier
progress_bar = window['progress']

while True:
    event, values = window.read()

    if event == "Close" or event == sg.WIN_CLOSED:
        break

    elif event == 'Execute Visualizer' and values['s1'] == True:

        sav_values = values #to grab the inputs
        from Statistics import figures_to_html
        html = threading.Thread(target = figures_to_html, args = (values[0] + ".html", values, progress_bar), daemon = True)
        html.run()

        #Loop until thread is done, then update it as done


        if not html.is_alive():
            progress_bar.update_bar(10)
            from Statistics import show_in_window
            vis = threading.Thread(target=show_in_window, args=(sav_values,))
            vis.run()


    elif event == 'Execute Visualizer' and values['s1'] == False:
        from Statistics import figures_to_html
        html = threading.Thread(target=figures_to_html, args=(values[0] + ".html", values, progress_bar))
        html.run()
        if not html.is_alive():
            progress_bar.update_bar(10)


window.close()

