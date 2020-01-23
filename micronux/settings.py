# module: settings.py
#
# setup settings classes


import micronux.definitions as df

class micron_setting:
    """generic micron setting"""

    def __init__(self, name, value):
        self.name = name.strip()
        self.value = value.strip()

        self.unit = False
        self.trim_val = self.value
        for key in df.units.keys():
            if self.value.endswith(key):
                self.unit = df.units[key]
                self.trim_val = self.value[:-len(key)]
            if self.value.startswith('x '):
                self.trim_val = self.value[2:]

        self.widget_name = self.name.replace(' ','_')

        self.type = self.widget_name.rsplit('_', 1)[-1]
        self.label = self.type
        if self.type in df.nicer_names:
            self.label = df.nicer_names[self.type]

        if self.widget_name.startswith('tracking_point_'):
            self.label = 'point '+self.type
            self.widget_name = self.widget_name.replace('-','m')
        if self.widget_name == 'fx1_fx2_balance':
            self.label = 'fx1|fx2  '
        if self.widget_name == 'lfo_1_mod_wheel_1':
            self.label = 'slider'

    def is_number(self, value):
        try:
            float(value)
        except ValueError:
            return False
        else:
            return True


    def normalise_val(self):
        if self.value == 'hold':
            return 30000001
        elif self.is_number(self.trim_val):
            if (not self.unit or self.unit == 'pct') and '.' in self.value:
                return int(float(self.trim_val) * 10)
            elif self.unit in df.unit_ratios.keys():
                ratio = df.unit_ratios[self.unit]
                return int(float(self.trim_val) * ratio)
            else:
                return int(round(float(self.trim_val)))
        else:
            return self.value


    def format_val(self, new_value):
        formated = ''
        if new_value == 30000001:
            formated = 'hold'
        elif is_number(new_value):
            if (not self.unit or self.unit == 'pct') and '.' in self.value:
                formated = str(new_value / 10)
            elif self.unit in df.unit_ratios.keys():
                ratio = df.unit_ratios[self.unit]
                formated = str(new_value / ratio)
            else:
                formated = str(new_value)
        else:
            formated = new_value
        if self.unit:
            for key,val in df.units.items():
                if val == self.unit:
                    formated += key
        if self.value.startswith('x '):
            formated = 'x '+formated
        return formated


    def disp_val(self, val):
        unit = ''
        if self.unit == 'pct':
            unit = '%'
        if (not self.unit or self.unit == 'pct') and '.' in self.value:
            val = int(val) / 10
        # show + sign when needed
        if self.type in df.mark_positive and (val > 0):
            val =  '+'+str(val)
        return str(val), unit


class micron_setting_time(micron_setting):
    """time setting"""
    def disp_val(self, val):
        if int(val) >= 500:
            roundings = 2
            if int(val) > 100000:
                roundings = 1
            disp = round(float(val/1000), roundings)
            unit = 'ms'
            if int(val) >= 1000000:
                roundings = 2
                if int(val) < 10000000:
                    roundings = 3
                disp = round(float(val/1000000), roundings)
                unit = 's'
        disp = str(disp).ljust(5, '0')
        if (self.widget_name.endswith('release_time')) or (self.widget_name.endswith('sus_time')):
            if int(val) > 30000000:
                disp = 'hold'
                unit = ''
        return  str(disp), unit


class micron_setting_frequency(micron_setting):
    """frequency setting"""
    def disp_val(self, val):
        if self.widget_name.endswith('offset_freq'):
            pad = 4
            if val < 0:
                pad = 5;
            disp = str(val/100).ljust(pad, '0')
            unit = ''
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
        return disp, unit


class micron_setting_pan(micron_setting):
    """pan setting"""
    def disp_val(self, val):
        unit = ''
        disp = str(val)
        if val < 0:
            disp = str(abs(val))
            unit = 'L'
        elif val > 0:
            unit = 'R'
        return disp, unit


class micron_setting_fm(micron_setting):
    """fm amount setting"""
    def disp_val(self, val):
        disp = str(val/10)
        unit = '%'
        return disp, unit


class micron_setting_balance(micron_setting):
    """x to y balance setting"""
    def disp_val(self, val):
        unit = '%'
        if (self.widget_name == 'extin_balance'):
            val = int((val+100)/2)
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

        return disp, unit


class micron_setting_mix(micron_setting):
    """mix setting"""
    def disp_val(self, val):
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
        return disp, unit


def factory(n,v):
    lword = n.rsplit(' ', 1)[-1]
    if lword == 'time':
        return micron_setting_time(n,v)
    elif (lword == 'freq') or (lword == 'rate'):
        return micron_setting_frequency(n,v)
    elif lword == 'pan':
        return micron_setting_pan(n,v)
    elif lword == 'amount':
        return micron_setting_fm(n,v)
    elif lword == 'balance':
        return micron_setting_balance(n,v)
    elif lword == 'mix':
        return micron_setting_mix(n,v)
    else:
        return micron_setting(n,v)
