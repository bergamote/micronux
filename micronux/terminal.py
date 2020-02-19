# module: terminal.py
#
# command line options


import sys, os.path, subprocess


default_prog = os.path.normpath('./programs/default.txt')

dec_path = os.path.normpath('./alesis/ion_program_decoder.pl')


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


### Check the command line arguments
def startup(args):
    # without argument, load the default program
    prog = default_prog
    if len(args) > 1:
        # create launcher option
        if args[1] == '--create-launcher':
            path = sys.path[0]
            l = "[Desktop Entry]\nType=Application\n"
            l += "Terminal=false\nName=Micronux\n"
            l += "Icon="+path+"/micronux/icon.png\n"
            l += "Exec=./micronux.py\n"
            l += "Categories=Application;\n"
            l += "GenericName=Micron Program Editor\n"
            l += "Path="+path
            launcher = open(path+'/micronux.desktop', 'w')
            launcher.write(l)
            launcher.close()
            subprocess.run(['chmod','+x', path+'/micronux.py'])
            subprocess.run(['chmod','+x', path+'/micronux.desktop'])
            sys.exit(0)
        # otherwise check if argument is a valid file
        elif os.path.isfile(args[1]):
            prog = args[1]
        else:
            print('Error opening "'+args[1]+'": File not found')
            sys.exit(1)
    return prog
