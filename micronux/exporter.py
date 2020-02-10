# module: importer.py
#
# save files


import subprocess
from micronux import converter, midi


newSettings = {}
convert_cache = './programs/cache/convert.txt'
auto = False


# Keep track of settings that changed
def setting_changed(ui):
    widget = ui.app.focusWidget()
    # workaround for radiobuttons
    if 'waveform' in widget.objectName():
        w_name = widget.objectName()
        if '1' in w_name:
            widget = ui.win.osc_1_waveform
        elif '2' in w_name:
            widget = ui.win.osc_2_waveform
        elif '3' in w_name:
            widget = ui.win.osc_3_waveform
    if not widget in newSettings:
        newSettings.update({widget.objectName(): widget})
        ui.win.ctrl_revert.setEnabled(True)
    if auto:
        auto_send(ui)


def auto_send(ui):
    if midi.send_ready:
        midi.send_ready = False
        txt = build_txt_file(ui.allSettings)
        syx = converter.txt_to_syx(txt)
        port = ui.win.ctrl_midi_port.currentText()
        if midi.interface(port, 'send', syx):
            midi.send_ready = True


def clear_changes(ui):
    newSettings.clear()
    ui.win.ctrl_revert.setEnabled(False)


def revert_changes(ui, allSettings):
    clear_changes(ui)
    ui.map_widgets(allSettings)
    if auto:
        auto_send(ui)
    ui.lcd_message('revert')


def build_line(widget, allSettings):
    setting = allSettings[widget.objectName()]
    if hasattr(widget, 'value'):
        new_value = widget.value()
    elif hasattr(widget, 'currentText'):
        new_value = widget.currentText()
    elif hasattr(widget, 'checkedButton'):
        new_value = widget
    elif hasattr(widget, 'checkState'):
        new_value = widget
    else:
        new_value = ''
    line = setting.name+': '
    line += str(setting.format_val(new_value))
    return line


def build_txt_file(allSettings):
    txt_file = '# Micron Program File\n'
    for setting in allSettings:
        if setting in newSettings:
            line = build_line(newSettings[setting], allSettings)
            txt_file += line+'\n'
        else:
            line = allSettings[setting].name+': '
            line += allSettings[setting].value
            txt_file += line+'\n'
    return txt_file


def save_file(file_path, allSettings):
    txt = build_txt_file(allSettings)
    if file_path.endswith('.txt'):
        txt_file = open(file_path, 'w')
        txt_file.write(txt)
        txt_file.close()
        return True
    elif file_path.endswith('.syx'):
        syx = converter.txt_to_syx(txt)
        syx_file = open(file_path, 'wb')
        syx_file.write(syx)
        syx_file.close()
        return True
    else:
        return False
