# module: mapwidgets.py
#
# Map settings to widgets.

from micronux.helpers import clean_val, disp_val, last_word
from micronux.helpers import keywords

def mapping(settings, app, window):

    print("### Mapping settings:")

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

                debug_line = 'QRadioButton -> '+waveform.objectName()
                debug_line += ': '+button_name+' ('+value+')'
                # print(debug_line)

    # Go through all the widgets,
    # if the name matches a setting name
    # assign the value to the widget.
    for widgoo in app.allWidgets():
        name = widgoo.objectName()
        if name in settings:
            widg_type = type(widgoo).__name__
            value = settings[name]
            if widg_type == 'QCheckBox':
                if (value == 'on') or (value == 'offset'):
                    widgoo.setChecked(True)
                elif (value == 'off') or (value == 'absolute'):
                    widgoo.setChecked(False)
            elif widg_type == 'QComboBox':
                keyword = value
                if value in keywords:
                    keyword = keywords[value]
                if value.startswith('x '):
                    keyword = value[2:]
                new_index = widgoo.findText(keyword)
                widgoo.setCurrentIndex(new_index)
            elif (widg_type == 'QDial') or (widg_type == 'QSlider'):
                if value != 'hold':
                    value = clean_val(value)
                else:
                    value = 30000001
                widgoo.setValue(value)
            elif (widg_type == 'QLabel') or (widg_type == 'QLineEdit'):
                widgoo.setText(value)

            debug_line = widg_type+' -> '+name+': '
            debug_line += str(value)+' ('+settings[name]+')'
            # print(debug_line)

    window.setWindowTitle(settings['name']+" | Micronux")
