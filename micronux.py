#! /usr/bin/python3
#
# A Python3/QT5 program editor for the Micron synth

import sys
from micronux import gui, trader, mapwidgets, lcd, effects
from micronux.definitions import easy_numbers


class mx():
    debug = True
    settings = trader.startup(sys.argv)
    changed_settings = []
    # setup app and window
    myQtGui = gui.make_gui('micronux/micronux.ui', 'Micronux', 'fusion')
    app = myQtGui['app']
    window = myQtGui['window']
    loaded = False


# set values to widgets
mapwidgets.load(mx.settings, mx.app, mx.window)

# Keep track of settings that changed
def setting_changed():
    if mx.loaded:
        widget = mx.app.focusWidget().objectName()
        if not widget in mx.changed_settings:
            mx.changed_settings.append(widget)
            print(mx.changed_settings)


# Update sliders values to 'lcd'
def pass_to_lcd():
    if mx.loaded:
        lcd.update(mx.app, mx.window, mx.settings)


# make title of fx toolbox tab reflect last selected fx
# and focus its tab
def fx_toolbox_title():
    if mx.loaded:
        tool_box = mx.window.fx_toolBox
        fx_widget = mx.app.focusWidget()
        if fx_widget.objectName() == 'fx_type':
            tool_box.setCurrentIndex(0)
            tool_box.setItemText(0,fx_widget.currentText())
        elif fx_widget.objectName() == 'fx2_type':
            tool_box.setCurrentIndex(1)
            tool_box.setItemText(1,fx_widget.currentText())


# Open file
def open_file():
    fname, _ = gui.QFileDialog.getOpenFileName(mx.window, 'Open file',
     './prog',"Sysex or Text Files (*.syx *.txt)")
    if fname:
        mx.settings = trader.import_file(fname)
        mx.loaded = False
        mapwidgets.load(mx.settings, mx.app, mx.window)
        mx.loaded = True
        mx.changed_settings.clear()

mx.window.actionOpen.triggered.connect(open_file)


# Connecting widgets
for widget in mx.app.allWidgets():
    widg_name = widget.objectName()
    widg_type = type(widget).__name__
    if widg_type in easy_numbers:
        widget.valueChanged.connect(setting_changed)
        # pass slider values to 'lcd'
        if (widg_type == 'QDial') or (widg_type == 'QSlider'):
            widget.valueChanged.connect(pass_to_lcd)
    elif widg_type == 'QComboBox':
        widget.currentIndexChanged.connect(setting_changed)
        if widg_name.startswith('fx') and widg_name.endswith('type'):
            widget.currentIndexChanged.connect(fx_toolbox_title)
    elif widg_type == 'QCheckBox':
        widget.stateChanged.connect(setting_changed)


# Test for pop up window
widgin = mx.window.widg_input
widgin.hide()

def close_widgin():
    widgin.hide()

def open_widgin():
    widgin.show()
    widgin.raise_()

mx.window.pushButton.clicked.connect(close_widgin)
mx.window.sh_widginPop.clicked.connect(open_widgin)


# Connect Quit menu
mx.window.actionQuit.triggered.connect(sys.exit)


mx.loaded = True

sys.exit(mx.app.exec_())
