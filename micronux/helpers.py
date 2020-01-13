# module: helpers.py
#
# Useful functions.

from micronux.definitions import units, percentages, keywords, mark_positive

# get the last word of string
def last_word(str):
    return str.rsplit('_', 1)[-1]

# get string value unit
def get_unit(str):
    unit = ''
    if str.endswith('% f1'):
        unit = 'bal'
    elif str.endswith('%'):
        unit = 'pct'
    elif str.endswith(' s'):
        unit = 's'
    elif str.endswith(' ms'):
        unit = 'ms'
    elif str.endswith(' Hz'):
        unit = 'hz'
    elif str.endswith(' KHz'):
        unit = 'khz'
    elif str.endswith('% fx1'):
        unit = 'fxbal'
    return unit

# make number strings into integer
def clean_val(val):
    if val == 'hold':
        return 30000001
    unit = get_unit(val)
    if unit == 'pct':
        if '.' in val:
            clean = float(val[:-1]) * 10
        else:
            clean = int(val[:-1])
    elif unit == 'ms':
        clean = int(float(val[:-3]) * 1000)
    elif unit == 's':
        clean = int(float(val[:-2]) * 1000000)
    elif unit == 'bal':
        clean = int(val[:-4])
    elif unit == 'fxbal':
        clean = int(val[:-5])
    elif unit == 'hz':
        clean = int(float(val[:-3]) * 1000)
    elif unit == 'khz':
        clean = int(float(val[:-4]) * 1000000)
    # the rest
    else:
        clean = int(round(float(val)))
    return clean

# make weird units into displayable value
def disp_val(val, setting):
    type = last_word(setting)
    unit = ''
    disp = str(val)

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

    # frequency
    elif (type == 'freq') or (type == 'rate'):
        if setting.endswith('offset_freq'):
            pad = 4
            if val < 0:
                pad = 5;
            disp = str(val/100).ljust(pad, '0')
        else:
            unit = 'hz'
            roundings = 2
            if int(val) > 100000:
                roundings = 1
            disp = round(float(val/1000), roundings)
            if int(val) >= 1000000:
                unit = 'khz'
                roundings = 2
                if int(val) < 10000000:
                    roundings = 3
                disp = round(float(val/1000000), roundings)
            disp = str(disp).ljust(5, '0')

    # left-right pan
    elif type == 'pan':
        if val < 0:
            disp = str(abs(val))
            unit = 'L'
        elif val > 0:
            unit = 'R'

    # fm amount
    elif type == 'amount':
        unit = '%'
        disp = str(val/10)

    # f1 to f2 balance
    elif type == 'balance':
        if (setting == 'extin_balance'):
            val = int((val+100)/2)
        unit = '%'
        f2 = str(val)
        f1 = str(100-val)
        separator = '|'
        if (val > 90) and (val < 100):
            f1 = ' '+f1
        if val == 0:
            disp = '100'
        elif val == 100:
            disp = '100  '
        else:
            disp = f2+separator+f1

    # wetdry mix
    elif type == 'mix':
        val = int((val+100)/2)
        unit = '%'
        dry = str(val)
        wet = str(100-val)
        separator = '|'
        if (val < 10) and (val > 0):
            dry = ' '+dry
        if val == 0:
            disp = '100  '
        elif val == 100:
            disp = '100'
        else:
            disp = wet+separator+dry

    # percents
    elif type in percentages:
        unit = '%'
    elif setting.startswith('tracking_point_'):
        unit = '%'

    # show + sign when needed
    if type in mark_positive and (val > 0):
        disp =  '+'+disp

    return (disp, unit)
