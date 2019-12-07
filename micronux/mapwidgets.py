# module: mapwidgets.py
# Map settings to widgets.

from micronux.helpers import clean_val, disp_val, last_word

debug = True
if debug:
    print("Mapping settings:")

def mapping(settings, app, window):

    # button groups (QRadioButton)
    waveform_groups = [
        window.osc_1_waveform,
        window.osc_2_waveform,
        window.osc_3_waveform
    ]

    for waveform in waveform_groups:
        for button in waveform.buttons():
            button_name = last_word(button.objectName())
            value = settings[waveform.objectName()]
            if value.startswith(button_name):
                button.toggle()

                if debug:
                    debug_line = 'QRadioButton -> '+waveform.objectName()
                    debug_line += ': '+button_name+' ('+value+')'
                    print(debug_line)

    # all other widgets
    for widgoo in app.allWidgets():
        name = widgoo.objectName()
        if name in settings:
            widg_type = type(widgoo).__name__
            value = settings[name]
            if widg_type == 'QCheckBox':
                if value == 'on':
                    widgoo.setChecked(True)
                elif value == 'off':
                    widgoo.setChecked(False)
            elif widg_type == 'QComboBox':
                new_index = widgoo.findText(value)
                widgoo.setCurrentIndex(new_index)
            elif (widg_type == 'QDial') or (widg_type == 'QSlider'):
                if value != 'hold':
                    value = clean_val(value)
                else:
                    value = 30000001
                widgoo.setValue(value)
            elif widg_type == 'QLabel':
                widgoo.setText(value)

            if debug:
                print(widg_type+' -> '+name+': '+str(value)+' ('+settings[name]+')')

    window.setWindowTitle(settings['name']+" | Micronux")
