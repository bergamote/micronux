# module: importer.py
#
# convert and save files

changed_settings = []

# Keep track of settings that changed
def setting_changed(ui):
    widget = ui.app.focusWidget()
    # workaround for radiobuttons
    if 'waveform' in widget.objectName():
        wave = widget.objectName()
        if '1' in wave:
            widget = ui.win.osc_1_waveform
        elif '2' in wave:
            widget = ui.win.osc_2_waveform
        elif '3' in wave:
            widget = ui.win.osc_3_waveform

    if not widget in changed_settings:
        changed_settings.append(widget)

def export_line(ui, allSettings):
    for widget in changed_settings:
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
            new_value = 'nope'
        line = setting.name+': '
        line += str(setting.format_val(new_value))
        print(line)
