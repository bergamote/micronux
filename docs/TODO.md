## To do / Roadmap

*Micronux*


#### Reduce combo boxes height

For x,y,z assign and inputs of sh, mods and tracking, the combo box is taller than the screen. Inputs should be broken down into groups and nested subgroups. ie:

- osc
  - 1
    - waveform
    - waveshape
    - etc...
  - 2
    - etc...


- midi cc
  - Spin box between 1 and 119

---


#### Non-linear sliders

Sliders for envelope times (attack, decay, release) need to have log curve applied to them so that small values are easier to select. Maybe also for lfo frequencies and filter rates. 

---

#### Disable "unheard" widgets

As already done with the effects sync setting.

- **porta** off, disable:
  - porta mode
  - porta type
  - time dial


- osc **sync** off, disable:
  - sync type
  - sync route


- filter = bypass, disable: 
  - freq dial
  - res dial
  - env amt dial
  - key track dial

- lfo/s&h,
  sync on: disables **rate** dial  
  sync off: disables **multiplier** selector

---


#### FXs: swap widget types

ie: replace reverb's **sync** dial by a checkbox.

---

#### Display tracking presets

Using the tracking parameter file from micronau as a base, display the tracking curve of selected preset.
https://github.com/retroware/micronau/blob/master/Source/tracking.h

---

### MIDI interactions

Wishfull thinking out loud:

- add a "pulse" option. Since sending a full sysex program stops the arpeggiator, latch, and held notes, it would be practical to send a midi note at regular interval to be able to hear the changes without having to press keys.

- request program sysex directly from within Micronux without having to select "send sysex" from the Micron. Possible if the user changes the program with Micronux linked before the request and we capture the program change msg. ("dwiddle that knob!" screen)

- show x,y and z knobs changes in Micronux. Also m1 and m2 sliders. First have to check what they are assigned to.

- convert to real time editor by sending single nrpn messages instead of the full sysex. micronau has a list of parameters with their sysex offset and nrpn, which could help: https://github.com/retroware/micronau/blob/master/Source/parameters.xml  
But still conversions to be done (7 bits?!)

----

## Reference

- [manual, firmware and presets](http://zine.r-massive.com/alesis-micron-archive/)  
- [sysex chart](http://forum.vintagesynth.com/viewtopic.php?f=1&t=113161)  
- [fandom wiki](https://ion-micron-miniak.fandom.com/wiki/Common_FAQ)  
- [micronau on github](https://github.com/retroware/micronau/)
