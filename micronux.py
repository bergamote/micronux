#! /usr/bin/python3
#
# A Python3/QT5 program editor for the Micron synth

import sys
from micronux import gui, trader, mapwidgets, lcd, effects, midi
from micronux.definitions import easy_numbers, get_button_groups
from PySide2.QtCore import QTimer

class mx():
    debug = True

    file_to_load = trader.startup(sys.argv)
    settings = trader.import_file(file_to_load)
    changed_settings = []

    # setup app and window
    myQtGui = gui.make_gui('micronux/micronux.ui', 'Micronux', 'fusion')
    app = myQtGui['app']
    win = myQtGui['window']
    loaded = False


# set values to widgets
mapwidgets.load(mx)
lcd.message(mx, 'startup')


# Keep track of settings that changed
def setting_changed():
    if mx.loaded:
        widget = mx.app.focusWidget()
        # workaround for radiobuttons
        if 'waveform' in widget.objectName():
            wave = widget.objectName()
            if '1' in wave:
                widget = mx.win.osc_1_waveform
            elif '2' in wave:
                widget = mx.win.osc_2_waveform
            elif '3' in wave:
                widget = mx.win.osc_3_waveform

        if not widget in mx.changed_settings:
            mx.changed_settings.append(widget)


# Update sliders values to 'lcd'
def pass_to_lcd():
    if mx.loaded:
        widg_type = type(mx.app.focusWidget()).__name__
        if (widg_type == 'QDial') or (widg_type == 'QSlider'):
            lcd.update(mx)

# Update fx tab, widgets and labels
def fx_switch():
    if mx.loaded:
        effects.switch(mx)

def clear_lcd():
    lcd.message(mx, 'clear')

# Test for pop up window
mx.win.pop.hide()

def close_widgin():
    mx.win.pop.hide()

def open_widgin():
    mx.win.pop.show()
    mx.win.pop.raise_()
    mx.win.lcdScreen.raise_()

def test_button():
    #test for export
    print('---------------')
    for widget in mx.changed_settings:
        value = 'new_value'
        line = trader.setting_to_text(widget.objectName(), value)
        print(line.strip())

mx.win.sh_widginPop.clicked.connect(test_button)


# Open file
def open_file():
    fname, _ = gui.QFileDialog.getOpenFileName(mx.win,
     'Open file', './prog',"Sysex or Text Files (*.syx *.txt)")
    if fname:
        mx.settings = trader.import_file(fname)
        mx.loaded = False
        mapwidgets.load(mx)
        mx.loaded = True
        mx.changed_settings.clear()
        lcd.message(mx, 'file_loaded')

mx.win.ctrl_open.clicked.connect(open_file)


# Receive sysex from Micron with menu bar 'Receive...'
def receive_interface():
    lcd.message(mx, 'receiving')
    open_widgin()
    QTimer.singleShot(0, receive_file)

def receive_file():
    port = mx.win.ctrl_midi_port.currentText()
    if midi.receive_sysex(port):
        mx.settings = trader.import_file(midi.cache)
        mx.loaded = False
        mapwidgets.load(mx)
        mx.loaded = True
        mx.changed_settings.clear()
        lcd.message(mx, 'receive_success')
    else:
        lcd.message(mx, 'receive_error')
    close_widgin()

mx.win.ctrl_receive.clicked.connect(receive_interface)


# Connecting buttongroups and widgets
radio_groups = get_button_groups(mx.win)

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


# Show and connect MIDI ports combobox
midi_ports = midi.list_midi_ports()
if len(midi_ports):
    for port in midi_ports:
        mx.win.ctrl_midi_port.addItems([port])
else:
    mx.win.ctrl_midi_port.addItems(['No MIDI port'])

def change_midi_port():
    port_name = mx.win.ctrl_midi_port.currentText()
    mx.midi_port = midi.check_midi_port(port_name)

mx.win.ctrl_midi_port.currentIndexChanged.connect(change_midi_port)


mx.loaded = True

sys.exit(mx.app.exec_())
