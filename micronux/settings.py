# module: settings.py
#
# setup settings class

import micronux.definitions as df

class micron_setting:
    """generic micron setting"""

    def __init__(self, name, value):
        self.name = name.strip()
        self.value = value.strip()

        self.unit = False
        self.clean_val = self.value
        for key in df.units.keys():
            if self.value.endswith(key):
                self.unit = df.units[key]
                self.clean_val = self.value[:-len(key)]
            if self.value.startswith('x '):
                self.clean_val = self.value[2:]

        self.widget_name = self.name.replace(' ','_')
        if self.widget_name.startswith('tracking_point_'):
            self.widget_name = self.widget_name.replace('-','m')

        self.type = self.widget_name.rsplit('_', 1)[-1]


    def is_number(self):
        try:
            float(self.clean_val)
        except ValueError:
            return False
        else:
            return True

    def normalise_val(self):
        if self.value == 'hold':
            return 30000001
        elif self.is_number():
            if (not self.unit or self.unit == 'pct') and '.' in self.value:
                return int(float(self.clean_val) * 10)
            elif self.unit in df.unit_ratios.keys():
                ratio = df.unit_ratios[self.unit]
                return int(float(self.clean_val) * ratio)
            else:
                return int(round(float(self.clean_val)))
        else:
            return self.value

    def format_val(self, new_value):
        formated = ''
        if self.value == 30000001:
            formated = 'hold'
        elif self.is_number():
            if (not self.unit or self.unit == 'pct') and '.' in self.value:
                formated = str(self.normalise_val() / 10)
            elif self.unit in df.unit_ratios.keys():
                ratio = df.unit_ratios[self.unit]
                formated = str(self.normalise_val() / ratio)
            else:
                formated = str(self.normalise_val())
        else:
            formated = self.value
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
        # show + sign when needed
        if type in df.mark_positive and (val > 0):
            val =  '+'+str(val)
        return str(val), unit, self.type

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
        return  str(disp), unit, self.type

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
            roundings = 2
            if int(val) > 100000:
                roundings = 1
            disp = round(float(val/1000), roundings)
            unit = 'hz'
            if int(val) >= 1000000:
                roundings = 2
                if int(val) < 10000000:
                    roundings = 3
                disp = round(float(val/1000000), roundings)
                unit = 'khz'
            disp = str(disp).ljust(5, '0')
        return disp, unit, self.type

class micron_setting_pan(micron_setting):
    """pan setting"""
    def disp_val(self, val):
        unit = ''
        if val < 0:
            disp = str(abs(val))
            unit = 'L'
        elif val > 0:
            unit = 'R'
        return disp, unit, self.type

class micron_setting_fm(micron_setting):
    """fm amount setting"""
    def disp_val(self, val):
        disp = str(val/10)
        unit = '%'
        return disp, unit, self.type

class micron_setting_balance(micron_setting):
    """x to y balance setting"""
    def disp_val(self, val):
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
        unit = '%'
        return disp, unit, self.type

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
        return disp, unit, self.type


txt_file = open('prog/received.txt', 'r')
settings_list = []
allSettings = {}
print('loading the new way')
for line in txt_file:
    line = line.strip()
    if line:
        if not line.startswith('#'): # remove comments
            pair = line.split(':')
            name = pair[0]
            value = pair[1]
            set = micron_setting(name, value)
            settings_list.append(set.widget_name)
            allSettings[set.widget_name] = set
txt_file.close()

for key in settings_list:
    set =  allSettings[key]
    if set.value != set.format_val(set.normalise_val()):
        print(set.name)
        print(set.value+' - '+set.format_val(set.value))
        print(set.disp_val(set.normalise_val()))

def setting_factory():
    return False
