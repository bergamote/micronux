# module: mapwidgets.py
#
# Map settings to widgets.

from micronux.helpers import clean_val, disp_val, last_word
import micronux.definitions as df
import micronux.effects as fx

def load(mx):
    settings, app, window = mx.settings, mx.app, mx.window
    # radio button groups (QRadioButton)
    radio_groups = df.get_button_groups(window)

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
                # display better dropdown choices
                keyword = value
                if value in df.keywords:
                    keyword = df.keywords[value]
                # we already write x symbol in QtDesigner
                if value.startswith('x '):
                    keyword = value[2:]

                new_index = widgoo.findText(keyword)
                widgoo.setCurrentIndex(new_index)

                if name == 'fx_type':
                    window.fx_toolBox.setItemText(
                        0, widgoo.currentText() )
                    fx.set_fx(mx, 1)
                    if widgoo.currentText() == 'bypass':
                        window.fx_toolBox.setCurrentIndex(1)
                if name == 'fx2_type':
                    window.fx_toolBox.setItemText(
                        1, widgoo.currentText() )
                    fx.set_fx(mx, 2)
                    if widgoo.currentText() == 'bypass':
                        window.fx_toolBox.setCurrentIndex(0)

            elif widg_type in df.easy_numbers:
                value = clean_val(value)
                widgoo.setValue(value)

            elif widg_type in df.easy_strings:
                widgoo.setText(value)

            debug_line = widg_type+' -> '+name+': '
            debug_line += str(value)+' ('+settings[name]+')'
            # print(debug_line)

    window.setWindowTitle(settings['name']+" | Micronux")
    window.output_level.setFocus()
