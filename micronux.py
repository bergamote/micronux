#! /usr/bin/python3
#
# A Python3/QT5 program editor for the Micron synth

import sys
from micronux import gui, trader, mapwidgets, lcd, effects
from micronux.definitions import easy_numbers, get_button_groups


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
mapwidgets.load(mx)

# Keep track of settings that changed
def setting_changed():
    if mx.loaded:
        widget = mx.app.focusWidget()
        # workaround for radiobuttons
        if 'waveform' in widget.objectName():
            wave = widget.objectName()
            if '1' in wave:
                widget = mx.window.osc_1_waveform
            elif '2' in wave:
                widget = mx.window.osc_2_waveform
            elif '3' in wave:
                widget = mx.window.osc_3_waveform

        if not widget in mx.changed_settings:
            mx.changed_settings.append(widget)


# Update sliders values to 'lcd'
def pass_to_lcd():
    if mx.loaded:
        lcd.update(mx)

# Update fx tab, widgets and labels
def fx_switch():
    if mx.loaded:
        effects.switch(mx)


# Open file
def open_file():
    fname, _ = gui.QFileDialog.getOpenFileName(mx.window,
     'Open file', './prog',"Sysex or Text Files (*.syx *.txt)")
    if fname:
        mx.settings = trader.import_file(fname)
        mx.loaded = False
        mapwidgets.load(mx)
        mx.loaded = True
        mx.changed_settings.clear()

mx.window.actionOpen.triggered.connect(open_file)


# Connecting buttongroups and widgets
radio_groups = get_button_groups(mx.window)

for group in radio_groups:
    group.buttonClicked.connect(setting_changed)

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
            widget.currentIndexChanged.connect(fx_switch)
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

    #test for export
    print('### changed settings')
    for widget in mx.changed_settings:
        value = 'new_value'
        line = trader.setting_to_text(widget.objectName(), value)
        print(line.strip())


mx.window.pushButton.clicked.connect(close_widgin)
mx.window.sh_widginPop.clicked.connect(open_widgin)


# Connect Quit menu
mx.window.actionQuit.triggered.connect(sys.exit)


mx.loaded = True

sys.exit(mx.app.exec_())
