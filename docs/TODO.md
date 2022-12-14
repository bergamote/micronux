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

Some sliders need to have a curve applied to them so that small values are easier to select.  
Following info from ION/MICRON PATCH DUMP SYSEX FORMAT By BEE (Bernard Escaillas 2008):

- **Filter cutoff freq**  
  {0...1022} = Herz where freq = exp( x / 147.933647)*20 Hz  
  {1023} = 20 000 Hz

- **Lfo and SH rate**  
  {0...1022} = Herz where rate = exp( x / 88.85677 ) / 100  
  {1023} = 1000 Hz

- **Effect 1 Lfo rate**  
  {0...1022} = Herz where rate = exp( x / 88.85677 ) / 100  
  {1023} = 1000 Hz


---

#### Disable "silent" widgets

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


- Lfo/SH:  
  sync on: disables **rate** dial  
  sync off: disables **multiplier** selector

---


#### Swap widget types on fx change

- replace **sync** and **shape** dials by checkboxes

- replace **synthesis** and **analysis** dials by 3 entry combo boxes

---

#### Tracking point presets

Display the curve of the currently selected tracking preset.  
Following info from micronau's [tracking.h](https://github.com/retroware/micronau/blob/master/Source/tracking.h):

- 12 points

      bypass : -100,-100,-100,-100,-100,-92,-83,-75,-67,-58,-50,-42,-33,-25,-17,-8,0,8,17,25,33,42,50,58,67,75,83,92,100,100,100,100,100
      negate : -100,-100,-100,-100,-100,-92,-83,-75,-67,-58,-50,-42,-33,-25,-17,-8,0,-8,-17,-25,-33,-42,-50,-58,-67,-75,-83,-92,-100,-100,-100,-100,-100
      absval : 100,100,100,100,100,92,83,75,67,58,50,42,33,25,17,8,0,8,17,25,33,42,50,58,67,75,83,92,100,100,100,100,100
      negabs : -100,-100,-100,-100,-100,-92,-83,-75,-67,-58,-50,-42,-33,-25,-17,-8,0,-8,-17,-25,-33,-42,-50,-58,-67,-75,-83,-92,-100,-100,-100,-100,-100
      exp+   : -100,-100,-100,-100,-100,-98,-96,-93,-90,-86,-80,-73,-64,-53,-39,-22,0,22,39,53,64,73,80,86,90,93,96,98,100,100,100,100,100
      exp-   : -100,-100,-100,-100,-100,-78,-61,-47,-36,-27,-20,-14,-10,-7,-4,-2,0,2,4,7,10,14,20,27,36,47,61,78,100,100,100,100,100

- 16 points

      bypass : -100,-94,-88,-81,-75,-69,-63,-56,-50,-44,-38,-31,-25,-19,-13,-6,0,6,13,19,25,31,38,44,50,56,63,69,75,81,88,94,100
      negate : 100,94,88,81,75,69,63,56,50,44,38,31,25,19,13,6,0,-6,-13,-19,-25,-31,-38,-44,-50,-56,-63,-69,-75,-81,-88,-94,-100
      absval : 100,94,88,81,75,69,63,56,50,44,38,31,25,19,13,6,0,6,13,19,25,31,38,44,50,56,63,69,75,81,88,94,100
      negabs : -100,-94,-88,-81,-75,-69,-63,-56,-50,-44,-38,-31,-25,-19,-13,-6,0,-6,-13,-19,-25,-31,-38,-44,-50,-56,-63,-69,-75,-81,-88,-94,-100
      exp+   : -100,-99,-97,-95,-93,-91,-88,-84,-80,-75,-69,-62,-53,-43,-31,-17,0,17,31,43,53,62,69,75,80,84,88,91,93,95,97,99,100
      exp-   : -100,-83,-69,-57,-47,-38,-31,-25,-20,-16,-12,-9,-7,-5,-3,-1,0,1,3,5,7,9,12,16,20,25,31,38,47,57,69,83,100

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
