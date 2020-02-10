# module: midi.py
#
# handle all MIDI stuff


import os.path, rtmidi


receive_cache = os.path.normpath('programs/cache/received.syx')
send_ready = True


def list_midi_ports():
    ''' List all midi ports, return a dict { name : address } '''
    md = rtmidi.RtMidiOut()
    port_list = {}
    for port in range(md.getPortCount()):
        name = md.getPortName(port)
        if not 'Through' in name:
            port_list[md.getPortName(port)] = port
    return port_list


def find_midi_port(port_name):
    ''' Check if a midi port name is valid and return its address'''
    port_list = list_midi_ports()
    if port_name in port_list.keys():
        return port_list[port_name]
    else:
        return False


def interface(port, action, syx=False):
    ''' Interface for midi send/receive sysex

        action 'receive'    saves file at
                            'receive_cache'
        action 'send'       send syx
        return True when done
    '''
    port = find_midi_port(port)
    if port:
        if action == 'receive':
            # wait in number of seconds
            # and/or midi messages
            waiting = 10
            received = False
            md = rtmidi.RtMidiIn()
            md.openPort(port)
            md.ignoreTypes(False, True, True)
            while waiting and not received:
                msg = md.getMessage(1000)
                if msg and validate_syx(msg):
                    save_syx(msg)
                    received = True
                    break
                waiting -= 1
            md.closePort()
            return received

        elif action == 'send':
            if not syx:
                return False
            else:
                md = rtmidi.RtMidiOut()
                md.openPort(port)
                msg = rtmidi.MidiMessage(syx)
                if validate_syx(msg):
                    md.sendMessage(msg)
                    return True
    else:
        print('MIDI port not valid')
        return False


def save_syx(msg):
    syx = open(receive_cache, 'bw')
    syx.write(msg.getRawData())
    syx.close()


def validate_syx(msg):
    if msg.isSysEx() and msg.getRawDataSize() == 434:
        return True
    else:
        return False
