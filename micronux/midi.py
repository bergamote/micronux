# module: midi.py
#
# handle all MIDI stuff


import os.path, rtmidi


receive_cache = os.path.normpath('programs/cache/received.syx')
send_cache = os.path.normpath('programs/cache/send.syx')
send_ready = True


def list_midi_ports():
    ''' List all midi ports, return a dict { name : address } '''
    md = rtmidi.RtMidiOut()
    port_list = {}
    for port in range(md.getPortCount()):
        port_list[md.getPortName(port)] = port
    return port_list


def find_midi_port(midi_port):
    ''' Check if a midi port name is valid and return its address'''
    port_list = list_midi_ports()
    if midi_port in port_list.keys():
        return port_list[midi_port]
    else:
        return False


def interface(action, port):
    ''' Interface for midi send/receive sysex

        actions can be 'send' or 'receive'
        return True when done
    '''
    port = find_midi_port(port)
    if port:
        if action == 'receive':
            md = rtmidi.RtMidiIn()
            md.openPort(port)
            md.ignoreTypes(False, True, True)
            msg = md.getMessage(10000)
            if msg:
                if msg.isSysEx() and msg.getRawDataSize() == 434:
                    syx = open(receive_cache, 'bw')
                    syx.write(msg.getRawData())
                    syx.close()
                    return True
            else:
                return False
        elif action == 'send':
            md = rtmidi.RtMidiOut()
            md.openPort(port)
            syx = open(send_cache, 'rb')
            msg = rtmidi.MidiMessage(syx.read())
            md.sendMessage(msg)
            return True
    else:
        print('MIDI port not valid')
        return False
