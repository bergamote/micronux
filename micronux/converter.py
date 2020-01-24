# module: importer.py
#
# convert files


import subprocess


ion_decoder_path = 'alesis/ion_program_decoder.pl'

# convert syx file to text file
# using ion_program_decoder.pl
def ipd(file_path):
    cmd = [ion_decoder_path, '-b', file_path]
    result = subprocess.run(cmd)
    if result.returncode == 0:
        return True
    else:
        return False
