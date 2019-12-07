# module: helpers.py
# Useful functions.

# get the last word of string
def last_word(str):
    return str.rsplit('_', 1)[-1]

units = {
'%': 'pct',
' s': 's',
' ms': 'ms',
' Hz': 'hz',
' KHz': 'khz'
}

# get string value unit
def get_unit(str):
    unit = ''
    if str.endswith('%'):
        unit = 'pct'
    elif str.endswith(' s'):
        unit = 's'
    elif str.endswith(' ms'):
        unit = 'ms'
    return unit

# make number strings into integer
def clean_val(val):
    unit = get_unit(val)
    if unit == 'pct':
        clean = int(val[:-1])
    elif unit == 'ms':
        clean = int(float(val[:-3]) * 1000)
    elif unit == 's':
        clean = int(float(val[:-2]) * 1000000)
    # the rest
    else:
        clean = int(round(float(val)))
    return clean

# make weird units into displayable value
def disp_val(val, setting):
    disp = str(val)
    type = last_word(setting)
    unit = ''

    # time
    if type == 'time':
        if int(val) >= 500:
            unit = 'ms'
            roundings = 2
            if int(val) > 100000:
                roundings = 1
            disp = round(float(val/1000), roundings)
            if int(val) >= 1000000:
                unit = 's'
                roundings = 2
                if int(val) < 10000000:
                    roundings = 3
                disp = round(float(val/1000000), roundings)
        disp = str(disp).ljust(5, '0')
        if (setting.endswith('release_time')) or (setting.endswith('sus_time')):
            if int(val) > 30000000:
                disp = 'hold'
                unit = ''

    # percents
    elif (type == 'level') or (type == 'shape'):
        unit = '%'

    return (disp, unit)
