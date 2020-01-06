#! /usr/bin/python3
#
# A Python3/QT5 program editor for the Micron synth

import sys, os.path, subprocess
from micronux import gui, trader, mapwidgets, lcd

debug = True

# Check the command line
args = sys.argv
if len(args) == 1:
    # Without argument, load the default program
    settings = trader.import_file('prog/default.txt')
else:
    # receive sysex option
    if args[1] == '-r':
        settings = trader.receive_file(args)
    # otherwise check if argument is a valid file
    elif os.path.isfile(args[1]):
        settings = trader.import_file(args[1])
    else:
        print('Error opening "'+args[1]+'": File not found')
        sys.exit(1)

# setup app and window
myQtGui = gui.make_gui('micronux/micronux.ui', 'Micronux', 'fusion')
app = myQtGui['app']
window = myQtGui['window']

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


window.actionQuit.triggered.connect(sys.exit)

sys.exit(app.exec_())
