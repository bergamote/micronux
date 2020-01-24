# module: importer.py
#
# open files


import os.path
from micronux import settings, converter


### Read text file and return settings
def text_file(file_path):
    settings_list = []
    allSettings = {}
    print('loading '+file_path)
    txt_file = open(file_path, 'r')
    for line in txt_file:
        line = line.strip()
        if line:
            if not line.startswith('#'): # remove comments
                if ':' in line:
                    pair = line.split(':')
                    name = pair[0]
                    value = pair[1]
                    set = settings.factory(name, value)
                    add_to_dict = {set.widget_name: set}
                    settings_list.append(set.widget_name)
                    allSettings.update(add_to_dict)
                else:
                    return False
    txt_file.close()
    return settings_list, allSettings


def open_file(file_path):
    if not os.path.isfile(file_path):
        return False
    else:
        if file_path.endswith('.syx'):
            convert_file = converter.ipd(file_path)
            if not convert_file:
                return False
            else:
                file_path = file_path[:-3]+'txt'
        if file_path.endswith('.txt'):
            return text_file(file_path)
        else:
            return False
