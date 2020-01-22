# module: midi.py
#
# Handle all MIDI stuff

import subprocess, os.path

cache = 'prog/received.syx'


### Check if MIDI port is valid
# return port address if it is
def check_midi_port(midi_port):
    ports_list = list_midi_ports()
    if midi_port in list(ports_list.keys()):
        return ports_list[midi_port]
    if midi_port in list(ports_list.values()):
        return midi_port
    else:
        return False

# List all midi ports
def list_midi_ports():
    result = subprocess.check_output(['amidi', '-l'])
    lines = (result.decode('ascii')).splitlines()
    lines.pop(0)
    ports = {}
    for line in lines:
        entry = line.split(None, 2)
        ports[entry[2]] = entry[1]
    return ports

### Receive sysex
def receive(port):
    # listen from amidi into cache file
    port = check_midi_port(port)
    if port:
        cmd = ['amidi', '-t', '4', '-p']
        cmd +=  [port, '-r', cache]
        print('listening at '+port)
        result = subprocess.run(cmd)
        if result.returncode == 0:
            if fix_syx(cache):
                return True
        else:
            # amidi shows error here
            return False
    else:
        print('MIDI port not valid')
        return False


### Fix syx function
# try to trim down sysex files when
# size is more than 434 bytes
def fix_syx(path):
    valid_syx = True
    size = os.path.getsize(path)
    if size > 434:
        with open(path, 'rb') as file:
            syx = file.read()
        start = syx.find(b'\xf0\x00')
        end = syx.find(b'\xf7')+1
        # if length between f0 00 and f7
        # is 434 byte, it's a micron sysex
        if (end - start) == 434:
            new_content = syx[start:end]
            # backup old sysex
            backup = open(path[:-4]+'_old.syx', 'wb')
            backup.write(syx)
            backup.close()
            fixed = open(path, 'wb')
            fixed.write(new_content)
            fixed.close()
        else:
            valid_syx = False
            print('wrong size sysex')
    elif size < 434:
        valid_syx = False
        print('wrong size sysex')
    return valid_syx
