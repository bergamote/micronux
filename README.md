# Micronux

**Micronux** is an editor for Linux to edit programs from the Alesis Micron synthesiser.  
It is just a front end to edit the text files generated by Alesis' program decoder/encoder perl script, and doesn't work in real time (but really close).


### Alpha

**Warning:** After receiving a program from the Micron, **save a backup copy** before pressing 'send' or enabling 'auto-send', as these options will **overwrite** the program on the Micron.


![screenshot of micronux](docs/screenshot.jpg)


### Features

  - Open and save `.syx` or `.txt` Micron program files.

  - Receive and send program sysex messages, selecting from a list of available MIDI ports.

  - Automatically send sysex on setting change.

  - Edit *almost* all program settings, including oscillators, envelopes, filters, mixers, effects, modulation routing, tracking generator and assign xyz knobs.


### Missing

  - see [to do list](docs/TODO.md)

  - Note that changes made on the Micron (with xyz knobs, slider, etc...) are *not* updated in Micronux.


### Install


You're gonna need python3, PySide2 and the pyrtmidi:

    pip3 install PySide2 rtmidi

Then simply run `./micronux.py` or make a launcher shortcut with:

    python3 ./micronux.py --create-launcher

Update to the latest version with `git pull`.


### Usage

To receive a sysex, make sure that the right MIDI port is selected then click `receive`. On the Micron bring up the `Send MIDI sysex?` option and press down the control knob.

Pressing `send` will **overwrite** the program with the same name on the Micron.

Ticking the checkbox next to `send` enables 'auto-send'.

The `revert` button *should* revert the changes made since the last open, save or receive.

The last received program is saved as `programs/cache/received.txt`.


### About

*Micronux* is written in **Python 3** and uses the **PySide2** bindings for its **QT** graphical interface, which is built using **QT Designer**. It uses **rtmidi** to send/receive sysex programs through MIDI.

The user interface is inspired by the physical layout of the Ion synthesiser as well as existing Mac/Windows editors. Since the amount of controls and settings of the Micron can be overwhelming, the goal is to simplify and promote the more commonly used settings.

Additionally, one goal is to keep Micronux functional on a netbook screen, so limited to a size of 1024x600 pixels.
