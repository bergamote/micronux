# module: lcd.py
#
# Updating the info display.

from micronux.helpers import clean_val, disp_val, last_word
from micronux.definitions import nicer_names

prev_setting = ''

# update display with value, unit and nice name
def update(mx):
    app, window, settings = mx.app, mx.window, mx.settings
    global prev_setting
    value = app.focusWidget().value()
    setting_name = app.focusWidget().objectName()
    nice_name = last_word(setting_name)

    # update value
    display_value = disp_val(value, setting_name)
    window.display_setting_value.setText(display_value[0])

    # update unit
    unit = display_value[1]
    window.display_setting_unit.setText(unit)

    # update name
    # look for a nicer name
    if nice_name in nicer_names:
        nice_name = nicer_names[nice_name]
    # exception for fx balance
    if setting_name == 'fx1_fx2_balance':
        nice_name = 'fx1|fx2  '
    if setting_name.startswith('tracking_point_'):
        nice_name = setting_name.replace('tracking_point_', 'point ')
        nice_name = nice_name.replace('m', '-')
    # only update display if name changed
    if prev_setting != setting_name:
        prev_setting = setting_name
        window.display_setting_name.setText(nice_name)

        # print('editing ' + setting_name)
