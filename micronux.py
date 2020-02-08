#! /usr/bin/python3
#
#   Micronux
#
# A program editor for the Micron synth


import sys
from micronux import gui, terminal, importer, exporter, midi, converter


class mx:
    startup_program = terminal.startup(sys.argv)
    allSettings = importer.open_file(startup_program)


ui = gui.micronux_ui(mx.allSettings)

ui.map_widgets(mx.allSettings, startup=True)

ui.win.show()
ui.lcd_message('startup')


# Open file
def open_file():
    fname, _ = gui.QtWidgets.QFileDialog.getOpenFileName(
        ui.win,
        'Open file',
        './programs/',
        "Sysex or Text Files (*.syx *.txt)")
    if fname:
        setup = importer.open_file(fname)
        if setup:
            mx.allSettings = setup
            ui.map_widgets(mx.allSettings)
            exporter.clear_changes(ui)
            ui.lcd_message('open_success')
        else:
            ui.lcd_message('open_error')
    ui.win.ctrl_auto_send.setChecked(False)

ui.win.ctrl_open.clicked.connect(open_file)


# Save file
def save_file():
    prog_name = mx.allSettings['name'].value
    fname, _ = gui.QtWidgets.QFileDialog.getSaveFileName(ui.win,
     'Save file', './programs/'+prog_name+'.txt',".syx or .txt (*.syx *.txt)")
    if fname:
        export = exporter.save_file(fname, mx.allSettings)
        if export:
            mx.allSettings = importer.open_file(fname)
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
    if midi.interface(port, 'receive'):
        setup = importer.open_file(midi.receive_cache)
        if setup:
            mx.allSettings = setup
            ui.map_widgets(mx.allSettings)
            exporter.clear_changes(ui)
            ui.lcd_message('receive_success')
    else:
        ui.lcd_message('receive_error')
    ui.pop_down()

ui.win.ctrl_receive.clicked.connect(pass_to_receive)


# Send sysex
def send_sysex():
    txt = exporter.build_txt_file(mx.allSettings)
    syx = converter.txt_to_syx(txt)
    port = ui.win.ctrl_midi_port.currentText()
    if midi.interface(port, 'send', syx):
        ui.lcd_message('send_success')
        return True
    else:
        ui.lcd_message('send_error')

ui.win.ctrl_send.clicked.connect(send_sysex)


# Auto-send
def set_auto_send():
    exporter.auto = ui.win.ctrl_auto_send.isChecked()
    if exporter.auto:
        ui.win.ctrl_send.setText('auto')
        ui.win.ctrl_send.setEnabled(False)
        exporter.auto_send(ui)
    else:
        ui.win.ctrl_send.setText('send')
        ui.win.ctrl_send.setEnabled(True)

ui.win.ctrl_auto_send.clicked.connect(set_auto_send)


# Revert changes
def revert():
    exporter.revert_changes(ui, mx.allSettings)

ui.win.ctrl_revert.clicked.connect(revert)



sys.exit(ui.app.exec_())
