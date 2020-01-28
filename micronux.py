#! /usr/bin/python3
#
#   Micronux
#
# A program editor for the Micron synth


import sys
from micronux import gui, terminal, importer, exporter, midi


class mx:
    file_to_load = terminal.startup(sys.argv)
    a, b = importer.open_file(file_to_load)
    settings_list = a
    allSettings = b

ui = gui.micronux_ui(mx.settings_list, mx.allSettings)

ui.map_widgets(mx.settings_list, mx.allSettings, connect=True)

ui.win.show()
ui.lcd_message('startup')


# Open file
def open_file():
    fname, _ = gui.QtWidgets.QFileDialog.getOpenFileName(ui.win,
     'Open file', './programs/',"Sysex or Text Files (*.syx *.txt)")
    if fname:
        setup = importer.open_file(fname)
        if setup:
            mx.settings_list, mx.allSettings = setup[0], setup[1]
            ui.map_widgets(mx.settings_list, mx.allSettings)
            exporter.clear_changes(ui)
            ui.lcd_message('open_success')
        else:
            ui.lcd_message('open_error')

ui.win.ctrl_open.clicked.connect(open_file)


# Save file
def save_file():
    prog_name = mx.allSettings['name'].value
    fname, _ = gui.QtWidgets.QFileDialog.getSaveFileName(ui.win,
     'Save file', './programs/'+prog_name+'.txt',".syx or .txt (*.syx *.txt)")
    if fname:
        export = exporter.save_file(fname, mx.settings_list, mx.allSettings)
        if export:
            exporter.clear_changes(ui)
            ui.lcd_message('save_success')
        else:
            ui.lcd_message('save_error')

ui.win.ctrl_save.clicked.connect(save_file)

# Receive sysex
def pass_to_receive():
    ui.lcd_message('receiving')
    ui.pop_up()
    ui.win.lcdScreen.raise_()
    gui.QTimer.singleShot(0, receive_sysex)

def receive_sysex():
    port = ui.win.ctrl_midi_port.currentText()
    if midi.interface('receive', port):
        setup = importer.open_file(midi.receive_cache)
        if setup:
            mx.settings_list, mx.allSettings = setup[0], setup[1]
            ui.map_widgets(mx.settings_list, mx.allSettings)
            exporter.clear_changes(ui)
            ui.lcd_message('receive_success')
    else:
        ui.lcd_message('receive_error')
    ui.pop_down()

ui.win.ctrl_receive.clicked.connect(pass_to_receive)


# Send sysex
def send_sysex():
    cache = exporter.save_file(midi.send_cache, mx.settings_list, mx.allSettings)
    if cache:
        port = ui.win.ctrl_midi_port.currentText()
        if midi.interface('send', port):
            return True
        else:
            ui.lcd_message('send_error')

ui.win.ctrl_send.clicked.connect(send_sysex)


# Revert changes
def revert():
    exporter.revert_changes(ui, mx.settings_list, mx.allSettings)

ui.win.ctrl_revert.clicked.connect(revert)



sys.exit(ui.app.exec_())
