### To do list
*micronux*

  
  - finish adding control widgets to ui:

      - effects: focus correct toolbox on effect change. Update a/b/c/... labels, change widget min/max value and swap widget when needed (ie: sync on/off with 2 radio buttons instead of a dial)

      - mods: pop-up window for sources and destination (combo box won't be practical)

      - arpegiator

      - assign knobs through pop-up window

      - improve sync combo box (how?)
      
  - add open/save functionality (detect automatically if file is syx or txt with extension).

  - option to rename programs.

  - receive and send programs with **amidi**.

  - button to revert modified program to synth received program.  

  - automatically send program on setting change. Note: when? on-release or every-second or what?

  - implement a non-linear slider for time (and maybe freq) related settings. Using a Log curve seems like a good way to go.

  - use *amidi* and *alsa conf* to make the midi port selectable from a menu. Automatically select if only one port.

  - reimplement the decoder/encoder perl script in python (maybe).

  - make a 1920x1080 layout with **Qt Designer** where all envelopes, effects, mods and tracking are visible. Maybe not a great idea (settings overload).

  - check if "send sysex..." can be triggered by cc. If yes, do the whole receive hands-off the micron.

  - add visual representation of oscillators, and everything else (if possible)!


----

### Reference

https://ion-micron-miniak.fandom.com/wiki/Common_FAQ
