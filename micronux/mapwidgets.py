# module: mapwidgets.py
#
# Map settings to widgets.

from micronux.helpers import clean_val, disp_val, last_word
from micronux.helpers import keywords

easy_numbers = [
'QDial',
'QSlider',
'QDoubleSpinBox'
]
easy_strings = [
'QLabel',
'QLineEdit'
]

def mapping(settings, app, window):

    print("### Mapping settings")

    # radio button groups (QRadioButton)
    radio_groups = [
        window.osc_1_waveform,
        window.osc_2_waveform,
        window.osc_3_waveform,
    ]

    for group in radio_groups:
        for button in group.buttons():
            button_name = last_word(button.objectName())
            value = settings[group.objectName()]
            if value.startswith(button_name):
                button.toggle()

                debug_line = 'QRadioButton -> '+group.objectName()
                debug_line += ': '+button_name+' ('+value+')'
                # print(debug_line)

    # Go through all the widgets,
    # if the name matches a setting name
    # assign the value to the widget.
    for widgoo in app.allWidgets():
        name = widgoo.objectName()
        widg_type = type(widgoo).__name__
        if name in settings:
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

            elif widg_type in easy_numbers:
                if value != 'hold':
                    value = clean_val(value)
                else:
                    value = 30000001
                widgoo.setValue(value)
            elif widg_type in easy_strings:
                widgoo.setText(value)

            debug_line = widg_type+' -> '+name+': '
            debug_line += str(value)+' ('+settings[name]+')'
            # print(debug_line)

        # Set labels for fx tabs
        if widg_type == 'QLabel':
            if name == 'label_fx_name':
                widgoo.setText(settings['fx_type'])
            if name == 'label_fx2_name':
                widgoo.setText(settings['fx2_type'])

    window.setWindowTitle(settings['name']+" | Micronux")
