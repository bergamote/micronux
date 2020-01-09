# module: lcd.py
#
# Updating the info display.

from micronux.helpers import clean_val, disp_val, last_word

debug = True

# setings better names for display
nicer_names = {
'semi':'semitone',
'fine':'cent',
'balance':'f1 | f2  ',
'mix':    'wet|dry  ',
'amount':'fm amount',
'freq':'frequency',
'res':'resonance',
'envamt':'env amount',
'wheel':'slider'
}

prev_setting = ''

# update display with value, unit and nice name
def update(app, window, settings):
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
    if setting_name == 'fx1_fx2_balance':
        nice_name = 'fx1|fx2  '
    # only update display if name changed
    if prev_setting != setting_name:
        prev_setting = setting_name
        window.display_setting_name.setText(nice_name)

        if debug:
            print('editing ' + setting_name)
