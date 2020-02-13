# module: importer.py
#
# open files


import os.path
from micronux import settings, terminal


### Read text file and return settings
def text_file(file_path):
    allSettings = {}
    txt_file = open(file_path, 'r')
    for line in txt_file:
        line = line.strip()
        if line:
            if not line.startswith('#'): # remove comments
                if ':' in line:
                    pair = line.split(':')
                    name = pair[0]
                    value = pair[1]
                    widget = settings.factory(name, value)
                    add_to_dict = {widget.widget_name: widget}
                    allSettings.update(add_to_dict)
    txt_file.close()
    return allSettings


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
            return text_file(file_path)
        else:
            return False
