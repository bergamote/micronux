# module: midi.py
#
# handle all MIDI stuff


import subprocess, os.path


receive_cache = 'programs/cache/received.syx'
send_cache = 'programs/cache/send.syx'
send_ready = True

### Check if MIDI port is valid
# return port address if it is
def find_midi_port(midi_port):
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


### interface for midi send/receive sysex
def interface(action, port):
    port = find_midi_port(port)
    if port:
        cmd = ['amidi', '-p', port]
        if action == 'receive':
            cmd += ['-t', '4', '-r', receive_cache]
        elif action == 'send':
            cmd += ['-s', send_cache]
        result = subprocess.run(cmd)
        if result.returncode == 0:
            if action == 'send':
                return True
            elif fix_syx(receive_cache):
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
            backup = open(path[:-4]+'-backup.syx', 'wb')
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
