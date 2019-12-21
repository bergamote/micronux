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
percentages = [
'level',
'shape',
'res',
'keytrack',
'envamt',
'drift',
'detune',
'wheel',
'smoothing',
'mix'
]

keywords = {
'positive': '+',
'negative': '-',
'filter 1 mix': 'f1 mix',
'filter 2 mix': 'f2 mix',
'3 -> 2 -> 1': '3 > 2 > 1',
'2+3 -> 1': '2+3 > 1',
'2 -> 1': '2 > 1',
'linear': 'lin'
}

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
    return unit

# make number strings into integer
def clean_val(val):
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
        if setting.endswith('extin_balance'):
            val = int((val+100)/2)
        unit = '%'
        f1 = str(val)
        f2 = str(100-val)
        separator = '|'
        if (val > 90) and (val < 100):
            f2 = ' '+f2
        disp = f1+separator+f2

    # percents
    elif type in percentages:
        unit = '%'

    return (disp, unit)
