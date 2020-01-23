
import sys, os.path, subprocess

from micronux import midi

ion_decoder_path = 'alesis/ion_program_decoder.pl'
default_prog = 'prog/default.txt'

### Check the command line arguments
def startup(args):
    # without argument, load the default program
    prog = default_prog
    if len(args) > 1:
        # receive sysex option
        if args[1] == '-r':
            try:
                # check if port given
                args[2]
            except:
                print('Please specify a MIDI port')
                sys.exit(1)
            else:
                if midi.receive_sysex(args[2]):
                    prog = midi.cache
        # create launcher option
        elif args[1] == '--create-launcher':
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
            subprocess.run(['chmod','+x', path+'/micronux.desktop'])
            sys.exit(0)
        # otherwise check if argument is a valid file
        elif os.path.isfile(args[1]):
            prog = args[1]
        else:
            print('Error opening "'+args[1]+'": File not found')
            sys.exit(1)
    return prog
