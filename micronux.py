#! /usr/bin/python3
#
# A Python3/QT5 program editor for the Micron synth

import sys
from micronux import gui, command_line, importer, exporter, midi
from PySide2.QtCore import QTimer

file_to_load = command_line.startup(sys.argv)

settings_list, allSettings = importer.open_file(file_to_load)

ui = gui.micronux_ui(settings_list, allSettings)

ui.connect_widgets()

ui.assign_values(settings_list, allSettings)

ui.win.show()


def pop_down():
    ui.win.pop.hide()

def pop_up():
    ui.win.pop.show()
    ui.win.pop.raise_()


def test_button():
    #test for export
    print('---------------')
    for widget in exporter.changed_settings:
        print(widget)

ui.win.test_button.clicked.connect(test_button)


# Open file
def open_file():
    fname, _ = gui.QFileDialog.getOpenFileName(ui.win,
     'Open file', './prog',"Sysex or Text Files (*.syx *.txt)")
    if fname:
        setup = importer.open_file(fname)
        if setup:
            settings_list, allSettings = setup[0], setup[1]
            ui.assign_values(settings_list, allSettings)
            exporter.changed_settings.clear()
            ui.lcd_message('file_loaded')
        else:
            ui.lcd_message('file_error')

ui.win.ctrl_open.clicked.connect(open_file)


# Receive sysex
def receive_interface():
    ui.lcd_message('receiving')
    pop_up()
    ui.win.lcdScreen.raise_()
    QTimer.singleShot(0, receive_sysex)

def receive_sysex():
    port = ui.win.ctrl_midi_port.currentText()
    if midi.receive(port):
        importer.open_file(midi.cache)
        
        exp.changed_settings.clear()
        ui.lcd_message('receive_success')
    else:
        ui.lcd_message('receive_error')
    pop_down()

ui.win.ctrl_receive.clicked.connect(receive_interface)


sys.exit(ui.app.exec_())
