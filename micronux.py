#! /usr/bin/python3
#
# A Python3/QT5 program editor for the Micron synth

import sys, os.path, subprocess
from micronux import gui, textfile, mapwidgets, lcd

debug = True

# setup app and window
myQtGui = gui.make_gui('micronux/micronux.ui', 'Micronux', 'fusion')
app = myQtGui['app']
window = myQtGui['window']

# amidi -l
midi_port = 'hw:2,0,0'

# import settings text file
file_name = 'prog/default'

if len(sys.argv) > 1:
    arg = sys.argv[1]
    if arg == '-r':
        cache = './prog/cache.syx'
        subprocess.run(['amidi', '-t', '3', '-p', midi_port, '-r',cache])
        file_name = cache
    elif not (arg.endswith('.txt') or arg.endswith('.syx')):
        print('File type must be .txt or .syx')
    else:
        if os.path.isfile(arg):
            file_name = arg
        else:
            print('File '+arg+' not found.')

print('### Loading '+file_name)
settings = textfile.import_file(file_name)

# set values to widgets
mapwidgets.mapping(settings, app, window)

# function to pass slider value to lcd
def pass_to_lcd():
    global app
    global window
    global settings
    lcd.update(app, window, settings)

# Connect sliders to LCD display.
for widget in app.allWidgets():
    widg_type = type(widget).__name__
    if (widg_type == 'QDial') or (widg_type == 'QSlider'):
        widget.valueChanged.connect(pass_to_lcd)

# Test for pop up window
widgin = window.widg_input
widgin.hide()

def close_widgin():
    widgin.hide()

def open_widgin():
    widgin.show()
    widgin.raise_()

window.pushButton.clicked.connect(close_widgin)
window.sh_widginPop.clicked.connect(open_widgin)


sys.exit(app.exec_())
