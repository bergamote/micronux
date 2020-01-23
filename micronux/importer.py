# module: importer.py
#
# open and convert files


import subprocess, sys, os.path
from micronux import settings, midi

ion_decoder_path = 'alesis/ion_program_decoder.pl'

# convert syx file to text file
# using ion_program_decoder.pl
def syx_to_txt(file_path):
    cmd = [ion_decoder_path, '-b', file_path]
    result = subprocess.run(cmd)
    if result.returncode == 0:
        return True
    else:
        return False


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
                    settings_list.append(set.widget_name)
                    allSettings[set.widget_name] = set
                else:
                    return False
    txt_file.close()
    return settings_list, allSettings


def open_file(file_path):
    if not os.path.isfile(file_path):
        return False
    else:
        if file_path.endswith('.syx'):
            convert_file = syx_to_txt(file_path)
            if not convert_file:
                return False
            else:
                file_path = file_path[:-3]+'txt'
        if file_path.endswith('.txt'):
            return text_file(file_path)
        else:
            return False
