#! /usr/bin/python3
#
# A Python3/QT5 program editor for the Micron synth

import sys, time, threading
from micronux import gui, trader, mapwidgets, lcd, effects
from micronux.definitions import easy_numbers, get_button_groups


class mx():
    debug = True
    settings = trader.startup(sys.argv)
    changed_settings = []
    # setup app and window
    myQtGui = gui.make_gui('micronux/micronux.ui', 'Micronux', 'fusion')
    app = myQtGui['app']
    win = myQtGui['window']
    loaded = False

    # for now midi port hard coded
    midi_port = 'hw:2,0,0'
    midi_cache = 'prog/received.syx'
    
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


# Test for pop up window
mx.win.pop.hide()

def close_widgin():
    mx.win.pop.hide()

def open_widgin():
    mx.win.pop.show()
    mx.win.pop.raise_()

    #test for export
    for widget in mx.changed_settings:
        value = 'new_value'
        line = trader.setting_to_text(widget.objectName(), value)
        print(line.strip())

mx.win.pop_pushButton.clicked.connect(close_widgin)
mx.win.sh_widginPop.clicked.connect(open_widgin)


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

mx.win.actionOpen.triggered.connect(open_file)


# Receive sysex needs threads to show timer countdown
def receive_file():
    mx.win.pop_label.setText('Receiving sysex...')
    mx.win.pop_pushButton.hide()
    open_widgin()

    thread_1 = threading.Thread(target=thread_receive_file)
    thread_2 = threading.Thread(target=receive_countdown)

    thread_1.start()
    thread_2.start()

def receive_countdown():
    for count in [4,3,2,1]:
        mx.win.pop_label_small.setText(str(count))
        time.sleep(1)

def thread_receive_file():
    sysex = trader.receive_sysex(mx)
    if sysex:
        mx.settings = sysex
        mx.loaded = False
        mapwidgets.load(mx)
        mx.loaded = True
        mx.changed_settings.clear()
    else:
        print('no sysex received')

    close_widgin()
    mx.win.pop_label.setText('')
    mx.win.pop_label_small.setText('')
    mx.win.pop_pushButton.show()

mx.win.actionReceive.triggered.connect(receive_file)


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


# Connect Quit menu
mx.win.actionQuit.triggered.connect(sys.exit)


mx.loaded = True

sys.exit(mx.app.exec_())
