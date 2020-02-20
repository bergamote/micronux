# module: importer.py
#
# open files


import os.path
from micronux import settings, terminal


### Read text file and return settings

def read_txt_file(setting_lines):
    settings_dic = {}
    for line in setting_lines:
        line_array = read_line(line)
        if line_array:
            name = line_array[0]
            value = line_array[1]
            settings_dic.update({name:value})
    return settings_dic


def read_line(line):
    line_array = []
    valid_line = False
    line = line.strip()
    if line:
        if not line.startswith('#'): # remove comments
            if ':' in line:
                pair = line.split(':')
                name = pair[0].strip()
                value = pair[1].strip()
                line_array.extend([name, value])
                valid_line = True
    if valid_line:
        return line_array
    else:
        return False


def open_file(file_path):
    if not os.path.isfile(file_path):
        return False
    else:
        if file_path.endswith('.syx'):
            convert_file = terminal.ipd(file_path)
            if not convert_file:
                return False
            else:
                file_path = file_path[:-3]+'txt'
        if file_path.endswith('.txt'):
            with open(file_path, 'r') as f:
                txt_file = f.readlines()
            setting_dic = read_txt_file(txt_file)
            allSettings = {}
            for name, value in setting_dic.items():
                widget = settings.factory(name, value)
                add_to_dict = {widget.widget_name: widget}
                allSettings.update(add_to_dict)
            return allSettings
        else:
            return False
