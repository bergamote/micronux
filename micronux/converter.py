# module: importer.py
#
# convert files


import subprocess


dec_path = 'alesis/ion_program_decoder.pl'


# convert syx file to text file
# using ion_program_decoder.pl
def ipd(file_path):
    cmd = [dec_path, '-b', file_path]
    result = subprocess.run(cmd)
    if result.returncode == 0:
        return True
    else:
        return False


def txt_to_syx(txt):
    perl_out = subprocess.check_output([dec_path, '-l', txt])
    hexa = perl_out.decode().strip().split('.')
    hexa = [item.rjust(2, '0') for item in hexa]
    hexa = bytes.fromhex(''.join(hexa))
    return hexa
