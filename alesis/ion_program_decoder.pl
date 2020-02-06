#! /usr/bin/perl
#
#-----------------------------------------------------------------------------
#
#  File:        ion_program_decoder.pl
#  Author:      Bret Victor
#  Date:        8/10/04
#
#  Usage:       ion_program_decoder.pl myprogram.syx
#               ion_program_decoder.pl myprogram.txt
#
#  Description: If given a .syx file, reads in a program and
#               and generates a .txt file that can be edited.
#               If given a .txt file, creates a .syx file that
#               contains the program described.
#
#  Copyright 2004 Alesis Studio Electronics. ALL RIGHTS RESERVED.
#
#-----------------------------------------------------------------------------

use strict;
use bytes;

#        1         2         3         4         5         6         7         8
sub usage { die <<_EOT_ }
Ion/Micron Program Decoder v1.00            (c) 2004 Alesis Studio Electronics

Converts Ion and Micron programs from sysex files to editable text files, and
vice versa.

usage: ion_program_decoder pgm.syx    : Generate description "pgm.txt".
       ion_program_decoder -b pgm.syx : Generate brief description "pgm.txt".
       ion_program_decoder pgm.txt    : Generate sysex "pgm.syx".
       
       ion_program_decoder -l '...'   : Takes text settings from the command
                                        line and prints sysex to stdout.
_EOT_


#-----------------------------------------------------------------------------
#  Default program description.
#-----------------------------------------------------------------------------
#  This is parsed before the actual txt file, so that parameters
#  omitted in the txt file get their default values.
#
my $default_program_txt = <<_EOT_;

#----------------------------------------
# Identification
#----------------------------------------

name:                 Program
ion location:         edit 0
micron file id:       0
category:             comp
knob x param:         Filter 1 Freq
knob y param:         Filter 1 Res
knob z param:         Post Fltr 1 Pan

#----------------------------------------
# Voice
#----------------------------------------

poly mode:            poly
unison:               off
unison voices:        2
unison detune:        0%
portamento:           off
portamento mode:      normal
portamento type:      fixed
portamento time:      160.223 ms
pitch wheel mode:     all
analog drift:         0%
osc sync:             off
osc sync type:        soft
osc sync route:       osc2
fm amount:            0.0%
fm algorithm:         2 -> 1
fm type:              linear

#----------------------------------------
# Oscillators
#----------------------------------------

osc 1 waveform:       sine
osc 2 waveform:       sine
osc 3 waveform:       sine
osc 1 shape:          0%
osc 2 shape:          0%
osc 3 shape:          0%
osc 1 octave:         0
osc 2 octave:         0
osc 3 octave:         0
osc 1 pitch semi:     0
osc 2 pitch semi:     0
osc 3 pitch semi:     0
osc 1 pitch fine:     0.0%
osc 2 pitch fine:     0.0%
osc 3 pitch fine:     0.0%
osc 1 p wheel range:  2
osc 2 p wheel range:  2
osc 3 p wheel range:  2

#----------------------------------------
# Prefilter Mix
#----------------------------------------

osc 1 level:          100%
osc 2 level:          0%
osc 3 level:          0%
ringmod level:        0%
noise level:          0%
extin level:          0%
osc 1 balance:        50% f1
osc 2 balance:        50% f1
osc 3 balance:        50% f1
ringmod balance:      50% f1
noise balance:        50% f1
extin balance:        0%
f1 to f2 level:       0%
noise type:           pink

#----------------------------------------
# Filters
#----------------------------------------

filter 1 type:        bypass
filter 2 type:        bypass
filter 1 freq:        10.000 KHz
filter 2 freq:        10.000 KHz
filter 1 res:         0%
filter 2 res:         0%
filter 1 keytrack:    100%
filter 2 keytrack:    100%
filter 1 envamt:      0%
filter 2 envamt:      0%
filter 2 absoffset:   absolute
filter 2 offset freq: 0.00
filter 1 level:       100%
filter 2 level:       0%
prefilter level:      0%
filter 1 pan:         0%
filter 2 pan:         0%
prefilter pan:        0%
filter 1 polarity:    positive
prefilter signal:     osc 1

#----------------------------------------
# Output
#----------------------------------------

drive type:           bypass
drive level:          0%
output level:         100%
effects wetdry mix:   -100%

#----------------------------------------
# Effects
#----------------------------------------

fx1 fx2 balance:      50% fx1
fx type:              bypass
fx param a:           100
fx param b:           79
fx param c:           87
fx param d:           100
fx param e:           0
fx param f:           0
fx param g:           0
fx param c synced:    x 1
fx2 type:             bypass
fx2 param a:          100
fx2 param b:          37
fx2 param c:          59
fx2 param d:          1
fx2 param a synced:   x 1

#----------------------------------------
# Envelopes
#----------------------------------------

env 1 attack time:    0.500 ms
env 2 attack time:    0.500 ms
env 3 attack time:    0.500 ms
env 1 attack slope:   lin
env 2 attack slope:   lin
env 3 attack slope:   lin
env 1 decay time:     0.500 ms
env 2 decay time:     0.500 ms
env 3 decay time:     0.500 ms
env 1 decay slope:    lin
env 2 decay slope:    lin
env 3 decay slope:    lin
env 1 sus time:       hold
env 2 sus time:       hold
env 3 sus time:       hold
env 1 sus level:      100%
env 2 sus level:      100%
env 3 sus level:      100%
env 1 release time:   2.000 ms
env 2 release time:   2.000 ms
env 3 release time:   2.000 ms
env 1 release slope:  lin
env 2 release slope:  lin
env 3 release slope:  lin
env 1 velocity:       0%
env 2 velocity:       0%
env 3 velocity:       0%
env 1 reset:          reset
env 2 reset:          reset
env 3 reset:          reset
env 1 freerun:        release
env 2 freerun:        release
env 3 freerun:        release
env 1 loop:           off
env 2 loop:           off
env 3 loop:           off
env 1 sus pedal:      on
env 2 sus pedal:      on
env 3 sus pedal:      on

#----------------------------------------
# LFOs
#----------------------------------------

lfo 1 tempo sync:     off
lfo 2 tempo sync:     off
lfo 1 rate:           8.003 Hz
lfo 2 rate:           8.003 Hz
lfo 1 synced rate:    x 16
lfo 2 synced rate:    x 8
lfo 1 reset:          mono
lfo 2 reset:          mono
lfo 1 mod wheel 1:    0%
lfo 2 mod wheel 1:    0%
sh tempo sync:        off
sh rate:              8.003 Hz
sh synced rate:       x 16
sh reset:             mono
sh input:             voice random
sh smoothing:         1%

#----------------------------------------
# Tracking Generator
#----------------------------------------

tracking input:       lfo 2 saw
tracking preset:      custom
tracking numpoints:   16
tracking point -16:   0%
tracking point -15:   0%
tracking point -14:   0%
tracking point -13:   0%
tracking point -12:   0%
tracking point -11:   0%
tracking point -10:   0%
tracking point -9:    0%
tracking point -8:    0%
tracking point -7:    0%
tracking point -6:    0%
tracking point -5:    0%
tracking point -4:    0%
tracking point -3:    0%
tracking point -2:    0%
tracking point -1:    0%
tracking point 0:     0%
tracking point 1:     0%
tracking point 2:     0%
tracking point 3:     0%
tracking point 4:     0%
tracking point 5:     0%
tracking point 6:     0%
tracking point 7:     0%
tracking point 8:     0%
tracking point 9:     0%
tracking point 10:    0%
tracking point 11:    0%
tracking point 12:    0%
tracking point 13:    0%
tracking point 14:    0%
tracking point 15:    0%
tracking point 16:    0%

#----------------------------------------
# Mod Matrix
#----------------------------------------

mod 1 source:         none
mod 2 source:         none
mod 3 source:         none
mod 4 source:         none
mod 5 source:         none
mod 6 source:         none
mod 7 source:         none
mod 8 source:         none
mod 9 source:         none
mod 10 source:        none
mod 11 source:        none
mod 12 source:        none
mod 1 dest:           none
mod 2 dest:           none
mod 3 dest:           none
mod 4 dest:           none
mod 5 dest:           none
mod 6 dest:           none
mod 7 dest:           none
mod 8 dest:           none
mod 9 dest:           none
mod 10 dest:          none
mod 11 dest:          none
mod 12 dest:          none
mod 1 level:          0.0%
mod 2 level:          0.0%
mod 3 level:          0.0%
mod 4 level:          0.0%
mod 5 level:          0.0%
mod 6 level:          0.0%
mod 7 level:          0.0%
mod 8 level:          0.0%
mod 9 level:          0.0%
mod 10 level:         0.0%
mod 11 level:         0.0%
mod 12 level:         0.0%
mod 1 offset:         0.0%
mod 2 offset:         0.0%
mod 3 offset:         0.0%
mod 4 offset:         0.0%
mod 5 offset:         0.0%
mod 6 offset:         0.0%
mod 7 offset:         0.0%
mod 8 offset:         0.0%
mod 9 offset:         0.0%
mod 10 offset:        0.0%
mod 11 offset:        0.0%
mod 12 offset:        0.0%

#----------------------------------------
# Ion Arpeggiator
#----------------------------------------

arp mode:             off
arp pattern:          1
arp tempo mult:       1
arp length:           2
arp octave range:     0
arp octave span:      up
arp note order:       forward
arp tempo:            1200

_EOT_

#-----------------------------------------------------------------------------
#  Ion program description.
#-----------------------------------------------------------------------------
#  If a dump is from Ion, this txt is used to set Micron-specific parameters
#  to their defaults.
#
my $ion_update_txt = <<_EOT_;

micron file id:       0
category:             comp
knob x param:         Filter 1 Freq
knob y param:         Filter 1 Res
knob z param:         Post Fltr 1 Pan

tracking preset:      custom
fx1 fx2 balance:      100% fx1
fx2 type:             bypass
fx2 param a:          100
fx2 param b:          37
fx2 param c:          59
fx2 param d:          1
fx2 param a synced:   x 1

_EOT_


#-----------------------------------------------------------------------------
#  Tables
#-----------------------------------------------------------------------------

#
#  First param in each category, for putting the category name in a comment.
#
my %categories = (
                   "poly mode"         => "Voice",
                   "osc * waveform"    => "Oscillators",
                   "osc 1 level"       => "Prefilter Mix",
                   "filter * type"     => "Filters",
                   "drive type"        => "Output",
                   "fx1 fx2 balance"   => "Effects",
                   "env * attack time" => "Envelopes",
                   "lfo * tempo sync"  => "LFOs",
                   "tracking input"    => "Tracking Generator",
                   "mod * source"      => "Mod Matrix",
                   "arp mode"          => "Ion Arpeggiator",
                  );

#
#  Parameter families with siblings.  These are used when the param name
#  has an * asterisk.
#
my %groups = (
               osc => [1 .. 3],
               filter => [1, 2],
               env => [1 .. 3],
               lfo => [1 .. 2],
               mod => [1 .. 12],
               knob => [qw(x y z)],
               "tracking point" => [-16 .. 16],
               "fx param" => [qw(a b c d e f g)],
              );

my $list_lfo_freq_sync =
   "x 16, x 12, x 10 2/3, x 8, x 6, x 5 1/3, x 4, x 3, x 2 2/3, x 2, ".
   "x 1 1/2, x 1 1/3, x 1, x 3/4, x 2/3, x 1/2, x 3/8, x 1/3, x 1/4, x 3/16, ".
   "x 1/6, x 1/8, x 3/32, x 1/12, x 1/16";

#
#  Parameter descriptions.  The min and max properties will be inferred if not given.
#  conv => "list" will be inferred if list => "..." is given.
#  If the name has an * asterisk, offset should be an arrayref or a coderef that
#  calculates the offset.
#
my @params = (

  { name => "micron file id", offset => 2360, min => 0, max => 16383, conv => "integer_16bit" },
  { name => "category", offset => 184, min => 2, list =>
      "recent, faves, bass, lead, pad, string, brass, key, comp, drum, sfx" },

  { name => "knob * param", offset => sub { 792 + 8*(ord($_[0])-ord('x')) }, list =>
      "Voice Polyphony, Voice Unison, Voice UsnDetune, Voice Portamnto, Voice PortaType, Voice PortaTime, ".
      "Voice Pitch Whl, Voice AnlgDrift, Voice Osc Sync, Voice FM Amount, Voice FM Type, Osc 1 Waveform, ".
      "Osc 1 Waveshape, Osc 1 Octave, Osc 1 Transpose, Osc 1 Pitch, Osc 1 PWhlRange, Osc 2 Waveform, ".
      "Osc 2 Waveshape, Osc 2 Octave, Osc 2 Transpose, Osc 2 Pitch, Osc 2 PWhlRange, Osc 3 Waveform, ".
      "Osc 3 Waveshape, Osc 3 Octave, Osc 3 Transpose, Osc 3 Pitch, Osc 3 PWhlRange, Pre Osc 1 Level, ".
      "Pre Osc 2 Level, Pre Osc 3 Level, Pre Ringm Level, Pre Noise Level, Pre ExtIn Level, Pre Osc 1 Balnc, ".
      "Pre Osc 2 Balnc, Pre Osc 3 Balnc, Pre Ringm Balnc, Pre Noise Balnc, Pre ExtIn Balnc, Pre Series Lvl, ".
      "Pre Noise Type, Filter 1 Type, Filter 1 Freq, Filter 1 Res, Filter 1 Keytrk, Filter 1 EnvAmt, ".
      "Filter 2 Offset, Filter 2 Type, Filter 2 Freq, Filter 2 Res, Filter 2 Keytrk, Filter 2 EnvAmt, ".
      "Post Fltr 1 Lvl, Post Fltr 2 Lvl, Post Preflt Lvl, Post Fltr 1 Pan, Post Fltr 2 Pan, Post Preflt Pan, ".
      "Post Preflt Src, Post Flt 1 Sign, Out Drive Type, Out Drive Level, Out Pgm Level, Out Fx Mix, ".
      "Env 1 Atk Time, Env 1 Atk Slope, Env 1 Dcy Time, Env 1 Dcy Slope, Env 1 Sus Time, Env 1 Sus Level, ".
      "Env 1 Rel Time, Env 1 Rel Slope, Env 1 Velocity, Env 1 Reset, Env 1 Freerun, Env 1 Loop, ".
      "Env 1 SusPedal, Env 2 Atk Time, Env 2 Atk Slope, Env 2 Dcy Time, Env 2 Dcy Slope, Env 2 Sus Time, ".
      "Env 2 Sus Level, Env 2 Rel Time, Env 2 Rel Slope, Env 2 Velocity, Env 2 Reset, Env 2 Freerun, ".
      "Env 2 Loop, Env 2 SusPedal, Env 3 Atk Time, Env 3 Atk Slope, Env 3 Dcy Time, Env 3 Dcy Slope, ".
      "Env 3 Sus Time, Env 3 Sus Level, Env 3 Rel Time, Env 3 Rel Slope, Env 3 Velocity, Env 3 Reset, ".
      "Env 3 Freerun, Env 3 Loop, Env 3 SusPedal, LFO 1 TempoSync, LFO 1 Rate, LFO 1 Reset, ".
      "LFO 1 M1 Slider, LFO 2 TempoSync, LFO 2 Rate, LFO 2 Reset, LFO 2 M1 Slider, S/H TempoSync, ".
      "S/H Rate, S/H Reset, S/H Input, S/H Smoothing, Track Input, Track Preset, ".
      "Track Grid, Track Point -16, Track Point -15, Track Point -14, Track Point -13, Track Point -12, ".
      "Track Point -11, Track Point -10, Track Point -9, Track Point -8, Track Point -7, Track Point -6, ".
      "Track Point -5, Track Point -4, Track Point -3, Track Point -2, Track Point -1, Track Center, ".
      "Track Point 1, Track Point 2, Track Point 3, Track Point 4, Track Point 5, Track Point 6, ".
      "Track Point 7, Track Point 8, Track Point 9, Track Point 10, Track Point 11, Track Point 12, ".
      "Track Point 13, Track Point 14, Track Point 15, Track Point 16, Category, Knob X Param, ".
      "Knob Y Param, Knob Z Param, Filter 2 Freq Offset, LFO 1 Rate Sync, LFO 2 Rate Sync, S/H Rate Sync" },

  { name => "poly mode", offset => 120, list => "mono, poly" },
  { name => "unison", offset => 121, list => "on, off" },
  { name => "unison voices", offset => 122, list => "2, 4, 8" },
  { name => "unison detune", offset => 128, conv => "percent" },

  { name => "portamento", offset => 135, list => "on, off" },
  { name => "portamento mode", offset => 152, list => "normal, legato" },
  { name => "portamento type", offset => 126, list => "fixed, scaled, gliss fixed, gliss scaled" },
  { name => "portamento time", offset => 136, max => 127, conv => "porta_time" },

  { name => "pitch wheel mode", offset => 144, list => "held, all" },
  { name => "analog drift", offset => 160, conv => "percent" },
  { name => "osc sync", offset => 278, list => "on, off" },
  { name => "osc sync type", offset => 280, list => "soft, hard" },
  { name => "osc sync route", offset => 279, list => "osc2, osc2+osc3" },

  { name => "fm amount", offset => 328, max => 1000, conv => "tenths_of_percent" },
  { name => "fm algorithm", offset => 282, list => "3 -> 2 -> 1, 2+3 -> 1, 2 -> 1" },
  { name => "fm type", offset => 295, list => "linear, exp" },

  { name => "osc * waveform", offset => [272, 284, 286], list => "sine, tri/saw, pulse" },
  { name => "osc * shape", offset => [240, 248, 256], min => -100, conv => "percent" },
  { name => "osc * octave", offset => [264, 296, 304], list => "-3, -2, -1, 0, 1, 2, 3" },
  { name => "osc * pitch semi", offset => [268, 300, 308], list =>
      "-7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7" },
  { name => "osc * pitch fine", offset => [200, 216, 232], min => -995, max => 995, conv => "pitch_fine" },
  { name => "osc * p wheel range", offset => [274, 312, 316], max => 12, conv => "integer" },

  { name => "osc 1 level", offset => 360, conv => "percent" },
  { name => "osc 2 level", offset => 368, conv => "percent" },
  { name => "osc 3 level", offset => 376, conv => "percent" },
  { name => "ringmod level", offset => 384, conv => "percent" },
  { name => "noise level", offset => 456, conv => "percent" },
  { name => "extin level", offset => 392, conv => "percent" },

  { name => "osc 1 balance", offset => 400, conv => "balance" },
  { name => "osc 2 balance", offset => 408, conv => "balance" },
  { name => "osc 3 balance", offset => 416, conv => "balance" },
  { name => "ringmod balance", offset => 424, conv => "balance" },
  { name => "noise balance", offset => 440, conv => "balance" },
  { name => "extin balance", offset => 432, min => -100, conv => "percent" },

  { name => "f1 to f2 level", offset => 448, conv => "percent" },
  { name => "noise type", offset => 463, list => "pink, white" },

  { name => "filter * type", offset => [608, 616], list =>
      "bypass, mg 4-pole lowpass, ob 2-pole lowpass, ob 2-pole bandpass, ob 2-pole highpass, ".
      "rp 4-pole lowpass, tb 3-pole lowpass, jp 4-pole lowpass, ".
      "8-pole lowpass, 8ve dual bandpass, 6-pole bandpass, phase warp, ".
      "comb filter 1, comb filter 2, vocal formant 1, vocal formant 2, vocal formant 3, ".
      "bandlimit, op 4-pole highpass, comb filter 3, comb filter 4" },
  { name => "filter * freq", offset => [512, 528], max => 1023, conv => "filter_freq" },
  { name => "filter * res", offset => [536, 544], conv => "percent" },
  { name => "filter * keytrack", offset => [576, 592], min => -100, max => 200, conv => "percent" },
  { name => "filter * envamt", offset => [552, 560], min => -100, conv => "percent" },
  { name => "filter 2 absoffset", offset => 600, list => "absolute, offset" },
  { name => "filter 2 offset freq", offset => 632, min => -400, max => 400, conv => "filter_offset_freq" },

  { name => "filter 1 level", offset => 664, conv => "percent" },
  { name => "filter 2 level", offset => 672, conv => "percent" },
  { name => "prefilter level", offset => 680, conv => "percent" },
  { name => "filter 1 pan", offset => 704, min => -100, conv => "percent" },
  { name => "filter 2 pan", offset => 712, min => -100, conv => "percent" },
  { name => "prefilter pan", offset => 720, min => -100, conv => "percent" },
  { name => "filter 1 polarity", offset => 696, list => "positive, negative" },
  { name => "prefilter signal", offset => 688, list => "osc 1, osc 2, osc 3, filter 1 mix, filter 2 mix, ringmod, noise" },

  { name => "drive type", offset => 776, list => 
       "bypass, compressor, rms limiter, tube overdrive, distortion, tube amp, fuzz pedal" },
  { name => "drive level", offset => 768, conv => "percent" },
  { name => "output level", offset => 784, conv => "percent" },
  { name => "effects wetdry mix", offset => 2240, min => -100, conv => "percent" },

  { name => "fx1 fx2 balance", offset => 2312, min => -50, max => 50, conv => "fx1_fx2_balance" },
  { name => "fx type", offset => 2232, list =>
     "bypass, super phaser, string phaser, theta flanger, thru 0 flanger, chorus, vocoder" },

  { name => "fx param *", offset => sub { 2248 + 8*(ord($_[0])-ord('a')) }, conv => "integer_8bit" },
  { name => "fx param c synced", offset => 2304, list => $list_lfo_freq_sync },

  { name => "fx2 type", offset => 2320, list =>
     "bypass, mono delay, stereo delay, split L/R delay, hall reverb, plate reverb, room reverb" },
  { name => "fx2 param a", offset => 736, conv => "integer_16bit" },
  { name => "fx2 param b", offset => 752, conv => "integer_16bit" },
  { name => "fx2 param c", offset => 1088, conv => "integer_16bit" },
  { name => "fx2 param d", offset => 1104, conv => "integer_16bit" },
  { name => "fx2 param a synced", offset => 1112, list => $list_lfo_freq_sync },

  { name => "env * attack time", offset => [840, 848, 856], max => 255, conv => "env_time" },
  { name => "env * attack slope", offset => [1056, 1064, 1072], list => "lin, exp+, exp-" },
  { name => "env * decay time", offset => [864, 872, 880], max => 255, conv => "env_time" },
  { name => "env * decay slope", offset => [1060, 1068, 1076], list => "lin, exp+, exp-" },
  { name => "env * sus time", offset => [920, 936, 952], max => 256, conv => "env_time" },
  { name => "env 1 sus level", offset => 888, conv => "percent" },
  { name => "env 2 sus level", offset => 896, min => -100, conv => "percent" },
  { name => "env 3 sus level", offset => 904, min => -100, conv => "percent" },
  { name => "env * release time", offset => [968, 984, 1000], max => 256, conv => "release_time" },
  { name => "env * release slope", offset => [1062, 1070, 1078], list => "lin, exp+, exp-" },
  { name => "env * velocity", offset => [1008, 1016, 1024], conv => "percent" },
  { name => "env * reset", offset => [1036, 1044, 1052], list => "reset, legato" },
  { name => "env * freerun", offset => [1038, 1046, 1054], list => "release, freerun" },
  { name => "env * loop", offset => [1032, 1040, 1048], list => "decay, zero, hold, off" },
  { name => "env * sus pedal", offset => [1035, 1043, 1051], list => "on, off" },

  { name => "lfo * tempo sync", offset => [1200, 1210], list => "on, off" },
  { name => "lfo * rate", offset => [1128, 1144], max => 1023, conv => "lfo_freq" },
  { name => "lfo * synced rate", offset => [1216, 1224], list => $list_lfo_freq_sync },
  { name => "lfo * reset", offset => [1240, 1244], list => "mono, poly, key mono, key poly, arp mono" },
  { name => "lfo * mod wheel 1", offset => [1152, 1160], conv => "percent" },

  { name => "sh tempo sync", offset => 1214, list => "on, off" },
  { name => "sh rate", offset => 1184, max => 1023, conv => "lfo_freq" },
  { name => "sh synced rate", offset => 1232, list => $list_lfo_freq_sync },
  { name => "sh reset", offset => 1192, list => "mono, poly, key mono, key poly, arp mono" },
  { name => "sh input", offset => 1168, list =>
      "note-on velocity, release velocity, key track, ".
      "m1 wheel, m2 wheel, pitch wheel, sustain pedal, expression pedal, ".
      "amp env level, filter env level, pitch/mod env level, ".
      "lfo 1 sine, lfo 1 cosine, lfo 1 triangle, lfo 1 cos-triangle, lfo 1 saw, lfo 1 cos-saw, lfo 1 square, lfo 1 cos-square, ".
      "lfo 2 sine, lfo 2 cosine, lfo 2 triangle, lfo 2 cos-triangle, lfo 2 saw, lfo 2 cos-saw, lfo 2 square, lfo 2 cos-square, ".
      "voice random, global random, portamento level, portamento effect, ".
      "tracking generator, step track, midi channel pressure, midi poly aftertouch, ".
      "midi cc 1, midi cc 2, midi cc 3, midi cc 4, midi cc 7, ".
      "midi cc 8, midi cc 9, midi cc 10, midi cc 11, midi cc 12, ".
      "midi cc 13, midi cc 14, midi cc 15, midi cc 16, midi cc 17, ".
      "midi cc 18, midi cc 19, midi cc 20, midi cc 21, midi cc 22, ".
      "midi cc 23, midi cc 24, midi cc 25, midi cc 26, midi cc 27, ".
      "midi cc 28, midi cc 29, midi cc 30, midi cc 31, midi cc 66, midi cc 67, ".
      "midi cc 68, midi cc 69, midi cc 70, midi cc 71, midi cc 72, ".
      "midi cc 73, midi cc 74, midi cc 75, midi cc 76, midi cc 77, ".
      "midi cc 78, midi cc 79, midi cc 80, midi cc 81, midi cc 82, ".
      "midi cc 83, midi cc 84, midi cc 85, midi cc 86, midi cc 87, ".
      "midi cc 88, midi cc 89, midi cc 90, midi cc 91, midi cc 92, ".
      "midi cc 93, midi cc 94, midi cc 95, midi cc 102, ".
      "midi cc 103, midi cc 104, midi cc 105, midi cc 106, midi cc 107, ".
      "midi cc 108, midi cc 109, midi cc 110, midi cc 111, midi cc 112, ".
      "midi cc 113, midi cc 114, midi cc 115, midi cc 116, midi cc 117, ".
      "midi cc 118, midi cc 119, key track extreme" },
  { name => "sh smoothing", offset => 1201, min => 1, conv => "percent" },

  { name => "tracking input", offset => 1912, list => 
      "note-on velocity, release velocity, key track, ".
      "m1 wheel, m2 wheel, pitch wheel, sustain pedal, expression pedal, ".
      "amp env level, filter env level, pitch/mod env level, ".
      "lfo 1 sine, lfo 1 cosine, lfo 1 triangle, lfo 1 cos-triangle, lfo 1 saw, lfo 1 cos-saw, lfo 1 square, lfo 1 cos-square, ".
      "lfo 2 sine, lfo 2 cosine, lfo 2 triangle, lfo 2 cos-triangle, lfo 2 saw, lfo 2 cos-saw, lfo 2 square, lfo 2 cos-square, ".
      "sh output, voice random, global random, portamento level, portamento effect, ".
      "midi channel pressure, midi poly aftertouch, ".
      "midi cc 1, midi cc 2, midi cc 3, midi cc 4, midi cc 7, ".
      "midi cc 8, midi cc 9, midi cc 10, midi cc 11, midi cc 12, ".
      "midi cc 13, midi cc 14, midi cc 15, midi cc 16, midi cc 17, ".
      "midi cc 18, midi cc 19, midi cc 20, midi cc 21, midi cc 22, ".
      "midi cc 23, midi cc 24, midi cc 25, midi cc 26, midi cc 27, ".
      "midi cc 28, midi cc 29, midi cc 30, midi cc 31, midi cc 66, midi cc 67, ".
      "midi cc 68, midi cc 69, midi cc 70, midi cc 71, midi cc 72, ".
      "midi cc 73, midi cc 74, midi cc 75, midi cc 76, midi cc 77, ".
      "midi cc 78, midi cc 79, midi cc 80, midi cc 81, midi cc 82, ".
      "midi cc 83, midi cc 84, midi cc 85, midi cc 86, midi cc 87, ".
      "midi cc 88, midi cc 89, midi cc 90, midi cc 91, midi cc 92, ".
      "midi cc 93, midi cc 94, midi cc 95, midi cc 102, ".
      "midi cc 103, midi cc 104, midi cc 105, midi cc 106, midi cc 107, ".
      "midi cc 108, midi cc 109, midi cc 110, midi cc 111, midi cc 112, ".
      "midi cc 113, midi cc 114, midi cc 115, midi cc 116, midi cc 117, ".
      "midi cc 118, midi cc 119, key track extreme" },
  { name => "tracking preset", offset => 2192, list =>
      "custom, bypass, negate, abs val, neg abs, exp+, exp-, zero, maximum, minimum" },
  { name => "tracking numpoints", offset => 1920, list => "12, 16" },
  { name => "tracking point *", offset => sub { 2056 + 8*$_[0] }, min => -100, conv => "percent" },

  { name => "mod * source", offset => sub { 1336 + 8*($_[0]-1) }, list =>
      "none, note-on velocity, release velocity, key track, ".
      "m1 wheel, m2 wheel, pitch wheel, sustain pedal, expression pedal, ".
      "amp env level, filter env level, pitch/mod env level, ".
      "lfo 1 sine, lfo 1 cosine, lfo 1 triangle, lfo 1 cos-triangle, lfo 1 saw, lfo 1 cos-saw, lfo 1 square, lfo 1 cos-square, ".
      "lfo 2 sine, lfo 2 cosine, lfo 2 triangle, lfo 2 cos-triangle, lfo 2 saw, lfo 2 cos-saw, lfo 2 square, lfo 2 cos-square, ".
      "sh output, voice random, global random, portamento level, portamento effect, ".
      "tracking generator, step track, midi channel pressure, midi poly aftertouch, ".
      "midi cc 1, midi cc 2, midi cc 3, midi cc 4, midi cc 7, ".
      "midi cc 8, midi cc 9, midi cc 10, midi cc 11, midi cc 12, ".
      "midi cc 13, midi cc 14, midi cc 15, midi cc 16, midi cc 17, ".
      "midi cc 18, midi cc 19, midi cc 20, midi cc 21, midi cc 22, ".
      "midi cc 23, midi cc 24, midi cc 25, midi cc 26, midi cc 27, ".
      "midi cc 28, midi cc 29, midi cc 30, midi cc 31, midi cc 66, midi cc 67, ".
      "midi cc 68, midi cc 69, midi cc 70, midi cc 71, midi cc 72, ".
      "midi cc 73, midi cc 74, midi cc 75, midi cc 76, midi cc 77, ".
      "midi cc 78, midi cc 79, midi cc 80, midi cc 81, midi cc 82, ".
      "midi cc 83, midi cc 84, midi cc 85, midi cc 86, midi cc 87, ".
      "midi cc 88, midi cc 89, midi cc 90, midi cc 91, midi cc 92, ".
      "midi cc 93, midi cc 94, midi cc 95, midi cc 102, ".
      "midi cc 103, midi cc 104, midi cc 105, midi cc 106, midi cc 107, ".
      "midi cc 108, midi cc 109, midi cc 110, midi cc 111, midi cc 112, ".
      "midi cc 113, midi cc 114, midi cc 115, midi cc 116, midi cc 117, ".
      "midi cc 118, midi cc 119, key track extreme" },

  { name => "mod * dest", offset => sub { 1432 + 8*($_[0]-1) }, list =>
     "none, voice pitch, osc 1 pitch full, osc 2 pitch full, osc 3 pitch full, ".
     "osc 1 pitch narrow, osc 2 pitch narrow, osc 3 pitch narrow, osc 1 shape, osc 2 shape, osc 3 shape, ".
     "osc fm level, osc 1 level, osc 2 level, osc 3 level, ring mod level, noise level, ext in level, ".
     "osc 1 balance, osc 2 balance, osc 3 balance, ring mod balance, noise balance, ext in balance, f1->f2 level, ".
     "portamento time, unison detune, filter 1 freq, filter 1 res, filter 1 env mod, filter 1 keytrack, ".
     "filter 2 freq, filter 2 res, filter 2 env mod, filter 2 keytrack, ".
     "lfo 1 rate, lfo 1 amplitude, lfo 2 rate, lfo 2 amplitude, s&h rate, s&h smoothing, s&h amplitude, ".
     "filter 1 level, filter 2 level, pre-filter level, filter 1 pan, filter 2 pan, pre-filter pan, ".
     "drive level, program level, main/aux balance, pan, ".
     "amp env amplitude, amp env rate, amp env attack, amp env decay, amp env sust time, amp env sust level, amp env release, ".
     "filter env amplitude, filter env rate, filter env attack, filter env decay, filter env sust time, filter env sust level, filter env release, ".
     "p/m env amplitude, p/m env rate, p/m env attack, p/m env decay, p/m env sust time, p/m env sust level, p/m env release, ".
     "dummy, ".
     "effects mix, effects parameter a, effects parameter b, effects parameter c, effects parameter d, ".
     "voice pitch narrow" },

  { name => "mod * level", offset => sub { 1536 + 16*($_[0]-1) }, min => -1000, max => 1000, conv => "tenths_of_percent" },
  { name => "mod * offset", offset => sub { 1728 + 16*($_[0]-1) }, min => -1000, max => 1000, conv => "tenths_of_percent" },

  { name => "arp mode", offset => 1278, list => "on, off, latch" },
  { name => "arp pattern", offset => 1256, max => 31, conv => "integer" },
  { name => "arp tempo mult", offset => 1261, list => "1/4, 1/3, 1/2, 1, 2, 3, 4" },
  { name => "arp length", offset => 1264, list => "2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16" },
  { name => "arp octave range", offset => 1268, max => 4, conv => "integer" },
  { name => "arp octave span", offset => 1272, list => "up, down, centered" },
  { name => "arp note order", offset => 1275, list => "forward, reverse, trigger, r-n-r in, r-n-r x, oct jump" },
  { name => "arp tempo", offset => 1288, min => 500, max => 2500, conv => "tenths" },

);


#-----------------------------------------------------------------------------
#  Conversion routines
#-----------------------------------------------------------------------------

my %limits;

sub conv_percent_to_txt   { $_[0] . "%" }
sub conv_percent_from_txt { ($_[0] =~ /^(\-?\d+)/)[0] }

sub conv_list_to_txt { (split /,\s*/, $_[1]->{list})[ $_[0] ] }
sub conv_list_from_txt {
    my $num = 0;
    my %hash;
    foreach (split /,\s*/, $_[1]->{list}) {
        s/\s//g;
        $hash{lc($_)} = $num++;
    }
    my $name = lc $_[0];
    $name =~ s/\s//g;
    return $hash{$name};
}

sub conv_tenths_of_percent_to_txt   { sprintf("%.1f%%", $_[0]/10) }
sub conv_tenths_of_percent_from_txt {
    $_[0] =~ /^(\-?\d+(\.\d)?)/ or return undef;
    my $result = $1 * 10;
    $result += ($result < 0) ? -0.5 : 0.5;
    return int($result);
}
$limits{max}->{tenths_of_percent} = 1000;

sub conv_tenths_to_txt   { sprintf("%.1f", $_[0]/10) }
sub conv_tenths_from_txt { conv_tenths_of_percent_from_txt(@_); }

sub conv_pitch_fine_to_txt   { conv_tenths_to_txt(@_) }
sub conv_pitch_fine_from_txt {
    my $tenths = conv_tenths_from_txt(@_);
    return $tenths - ($tenths % 5);
}

sub conv_balance_to_txt   { (50 - $_[0]) . "\% f1" }
sub conv_balance_from_txt {
    $_[0] =~ /^(\-?\d+)/ or return undef;
    return 50 - $1;
}
$limits{min}->{balance} = -50;
$limits{max}->{balance} =  50;

sub conv_fx1_fx2_balance_to_txt { (50 - $_[0]) . "\% fx1" }
sub conv_fx1_fx2_balance_from_txt { conv_balance_from_txt(@_) }

sub conv_filter_offset_freq_to_txt { sprintf "%.2f", $_[0]/100; }
sub conv_filter_offset_freq_from_txt {
    $_[0] =~ /^(\-?\d+(\.\d+)?)/ or return undef;
    my $result = $1 * 100;
    $result += ($result < 0) ? -0.5 : 0.5;
    return int($result);
}

sub logscale {
    my ($value, $minvalue, $maxvalue, $maxoutput) = @_;
    return int(0.5 + (log($value/$minvalue)/log($maxvalue/$minvalue) * $maxoutput));
}
sub hz_to_string {
    my ($hz) = @_;
    if ($hz >= 1000) { return sprintf "%.3f KHz", $hz/1000 }
    else { return sprintf "%.3f Hz", $hz }
}
sub string_to_hz {
    my ($string) = @_;
    (lc $string) =~ /^(\d+(\.\d+)?) \s* (k?)hz/x or return undef;
    my $hz = $1;
    $hz *= 1000 if $3;
    return $hz;
}

sub conv_filter_freq_to_txt {
    return "10.000 KHz" if $_[0] == 920;
    my $hz = 20 * 1000 ** ($_[0]/1023);
    return hz_to_string($hz);
}
sub conv_filter_freq_from_txt {
    my $hz = string_to_hz($_[0]) || return undef;
    return logscale($hz, 20, 20000, 1023);
}

sub conv_lfo_freq_to_txt {
    my $hz = 0.01 * (1000/0.01) ** ($_[0]/1023);
    return hz_to_string($hz);
}
sub conv_lfo_freq_from_txt {
    my $hz = string_to_hz($_[0]) || return undef;
    return logscale($hz, 0.01, 1000, 1023);
}

sub ms_to_string {
    my ($ms) = @_;
    if ($ms >= 1000) { return sprintf "%.3f s", $ms/1000 }
    else { return sprintf "%.3f ms", $ms }
}
sub string_to_ms {
    my ($string) = @_;
    (lc $string) =~ /^(\d+(\.\d+)?) \s* (m?)s/x or return undef;
    my $ms = $1;
    $ms *= 1000 unless $3;
    return $ms;
}

sub conv_env_time_to_txt {
    return "hold" if $_[0] == 256;
    my $ms = 0.5 * (30000/0.5) ** ($_[0]/255);
    return ms_to_string($ms);
}
sub conv_env_time_from_txt {
    $_[0] =~ /hold/i and return 256;
    my $ms = string_to_ms($_[0]) || return undef;
    return logscale($ms, 0.5, 30000, 255);
}

sub conv_release_time_to_txt {
    return "hold" if $_[0] == 256;
    my $ms = 2 * (30000/2) ** ($_[0]/255);
    return ms_to_string($ms);
}
sub conv_release_time_from_txt {
    $_[0] =~ /hold/i and return 256;
    my $ms = string_to_ms($_[0]) || return undef;
    return logscale($ms, 2, 30000, 255);
}

sub conv_porta_time_to_txt {
    my $ms = 10 * (1000) ** ($_[0]/127);
    return ms_to_string($ms);
}
sub conv_porta_time_from_txt {
    my $ms = string_to_ms($_[0]) || return undef;
    return logscale($ms, 10, 10000, 127);
}

sub conv_integer_to_txt       { $_[0] }
sub conv_integer_8bit_to_txt  { $_[0] }
sub conv_integer_16bit_to_txt { $_[0] }
sub conv_integer_from_txt     { ($_[0] =~ /^(\-?\d+)/)[0] }
sub conv_integer_8bit_from_txt  { conv_integer_from_txt(@_) }
sub conv_integer_16bit_from_txt { conv_integer_from_txt(@_) }
$limits{min}->{integer_8bit} = -(1 << 7);
$limits{max}->{integer_8bit} =  (1 << 7) - 1;
$limits{min}->{integer_16bit} = -(1 << 15);
$limits{max}->{integer_16bit} =  (1 << 15) - 1;

#
#  Infer parameters that are not given.
#
foreach (@params) {
    if (exists $_->{list}) {
        $_->{conv} = "list";
        $_->{max} = ($_->{list} =~ tr/,//) unless defined $_->{max};
        $_->{min} = 0 unless defined $_->{min};
    }
    else {
        for my $key (qw(max min)) {
            unless (exists $_->{$key}) {
                my $limit = $limits{$key}->{$_->{conv}};
                defined $limit or $limit = ($key eq 'max' ? 100 : 0);
                $_->{$key} = $limit;
            }
        }
    }
}

#
#  Create a %paramlookup hash that maps fully-qualified param names
#  (no asterisks) to a copy of the param hash with the correct offset.
#
my %paramlookup;
for my $param (@params) {
    foreach_param($param, sub {
       my ($name, $offset) = @_;
       $paramlookup{$name} = { %$param, offset => $offset };
    });
}


#-----------------------------------------------------------------------------
#  Fancy parameters that can't use normal conversion routines
#-----------------------------------------------------------------------------

my $global_sysex_opcode;
my $byte_offset_to_name_in_dependency_list = 296;
my %special_dump_writers = (
  name => sub {
      my ($dumpref, $value) = @_;
      $value =~ s/[^\x20-\x7f]/ /g;
      unless ($value =~ /\S/) { $value = "Program" }
      my $name = substr $value . (chr(0) x 14), 0, 14;
      $name .= chr(0);
      substr $$dumpref, 0, 15, $name;                                                # main name
      substr $$dumpref, $byte_offset_to_name_in_dependency_list,    15, $name;       # dependency list name
      substr $$dumpref, $byte_offset_to_name_in_dependency_list - 4, 2, "\x00\x01";  # dependency filetype (program)
  },
  "ion location" => sub {
      my ($dumpref, $value) = @_;
      my ($bank, $slot) = split ' ', lc $value;
      defined $slot or return;
      my %hash = (red => 0, green => 1, blue => 2, user => 3, edit => 4);
      my $banknum = $hash{$bank};
      defined $banknum or $banknum = $hash{edit};
      $slot = 0 unless $slot =~ /^\d+$/;
      $slot = 0 if $banknum == $hash{edit} and $slot > 3;
      $global_sysex_opcode = (((1 << 8) + $banknum) << 16) + $slot;
  },

);

sub is_program_from_micron {
    my ($dump) = @_;
    return (substr($dump, 0, 14) eq substr($dump, $byte_offset_to_name_in_dependency_list, 14));
}

#-----------------------------------------------------------------------------
#  Subroutines
#-----------------------------------------------------------------------------

# If param is a family (name has asterisk) call sub for each sibling.
# If param is normal, call sub for it normally.
sub foreach_param {
    my ($param, $sub) = @_;
    my $name = $param->{name};
    if ($name !~ /(.+?)\s+\*/) {
        $sub->($name, $param->{offset});
    }
    else {
        my $range = $groups{$1};
        for my $num (@$range) {
            my $realname = $name;
            $realname =~ s!\*!$num!;
            my $offset;
            if (ref($param->{offset}) =~ /ARRAY/) {
                $offset = $param->{offset}->[$num - 1];
            } else {
                $offset = $param->{offset}->($num);
            }
            $sub->($realname, $offset);
        }
    }
}

sub get_location_from_opcode {
    my ($opcode) = @_;
    my $bank = (qw(red green blue user edit edit edit edit))[($opcode >> 16) & 7];
    my $slot = $opcode & 127;
    if ($bank eq 'edit' and $slot > 3) { $slot = 0; }
    return "$bank $slot";
}

sub get_bitwidth_of_param {
    my ($min, $max) = @_;
    my $biggest = (($max+1) > -$min) ? ($max+1) : -$min;
    my $bits = int(log($biggest)/log(2) + 0.99999);
    $bits++ if $min < 0;
    return $bits;
}

sub write_param_to_dump {
    my ($dumpref, $offset, $min, $max, $value) = @_;

    my $bits = get_bitwidth_of_param($min, $max);
    my $byte_offset = int($offset / 8);

    if ($value < $min) { $value = $min; }
    if ($value > $max) { $value = $max; }

    if ($bits >= 8 or $min < 0) {
        # Write low byte.
        substr $$dumpref, $byte_offset, 1, chr($value & 0xff);
    }
    if ($bits > 8) {
        # Write high byte (big-endian).
        substr $$dumpref, $byte_offset - 1, 1, chr(($value >> 8) & 0xff);
    }
    if ($bits < 8 and $min >= 0) {
        # Write into bitfield.
        my $mask = ((1 << $bits) - 1) << ($offset % 8);
        my $old = substr $$dumpref, $byte_offset, 1;
        my $new = chr(  (ord($old) & (~$mask & 0xff)) | ($value << ($offset % 8)) );
        substr $$dumpref, $byte_offset, 1, $new;
    }
}

sub read_param_from_dump {
    my ($dump, $offset, $min, $max) = @_;

    my $bits = get_bitwidth_of_param($min, $max);
    my $byte_offset = int($offset / 8);

    # Read low byte.
    my $result = ord(substr($dump, $byte_offset, 1));
    if ($bits > 8) {
        # Read high byte (big-endian).
        $bits = 16;
        $result += 256 * ord(substr($dump, $byte_offset - 1, 1));
    }
    elsif ($bits < 8) {
        # All negative params are either 8 or 16 bits.
        if ($min < 0) { $bits = 8; }
        else {
            # Shift and mask param in bitfield.
            $result >>= $offset % 8;
            $result &= ((1 << $bits) - 1);
        }
    }
    # Extend sign bit if negative.
    if ($min < 0 && ($result & (1 << ($bits - 1)))) {
        $result = -(-$result & ((1 << $bits) - 1));
    }
    # Clip to valid range.
    if ($result < $min) { $result = $min; }
    if ($result > $max) { $result = $max; }
    return $result;
}

sub call_conversion_function {
    my ($param, $value, $to_or_from) = @_;
    my $func = "conv_" . $param->{conv} . "_${to_or_from}_txt";
    # Call conversion function through symbolic reference.
    no strict;
    eval { $func->($value, $param) };
}

sub get_formatted_value {
    my ($param, $raw_value) = @_;
    call_conversion_function($param, $raw_value, "to");
}

sub get_raw_value {
    my ($param, $formatted_value) = @_;
    call_conversion_function($param, $formatted_value, "from");
}

sub pretty_print {
    my ($name, $value) = @_;
    return "$name: " . (" " x (20 - length $name)) . "$value\n";
}

sub banner_print {
    my (@strings) = @_;
    my $txt = "\n#".("-" x 40)."\n";
    $txt .= "# $_\n" foreach @strings;
    $txt .= "#".("-" x 40)."\n\n";
    return $txt;
}

sub verbose_print {
    my ($param) = @_;
    if ($param->{conv} ne 'list') {
        my $min = get_formatted_value($param, $param->{min});
        my $max = get_formatted_value($param, $param->{max});
        return qq(# "$param->{name}" can range from $min to $max\n);
    }
    else {
        my @list = split /,\s*/, $param->{list};
        my $text = qq(# "$param->{name}" can be:\n);
        my $line = "";
        foreach (@list[ $param->{min} .. $param->{max} ], undef) {
            if (!defined or length($line . $_) > 72) {
                $text .= "#   $line\n";
                $line = "";
            }
            last unless defined;
            $line .= $_;
            $line .= ", " unless $_ eq $list[-1];
        }
        if (length $text < 72 and $text =~ tr/\n// == 2) {
            $text =~ s/\n# //;
        }
        return $text;
    }
}

sub build_dump_from_txt {
    my ($dumpref, $txt) = @_;

    foreach (split /\n/, $txt) {
        next if /^#/ or /^\s*$/;
        my ($name, $formatted_value) = /^ \s* ([\-\w ]+?) \s* : \s* (\S.*)? $/x;
        $name or warn("I did not understand this line:\n$_\n"), next;
        defined $formatted_value or warn("You did not give a value for the \"$name\" param.\n"), next;
        my $dump_writer = $special_dump_writers{$name};
        if ($dump_writer) { $dump_writer->($dumpref, $formatted_value); }
        else {
            my $param = $paramlookup{$name} or warn("I don't know what the \"$name\" param is.\n"), next;
            my $raw_value = get_raw_value($param, $formatted_value);
            defined $raw_value or warn("\"$formatted_value\" is not a valid value for the \"$name\" param.\n"), next;
            write_param_to_dump($dumpref, $param->{offset}, $param->{min}, $param->{max}, $raw_value);
        }
    }
}


my $sysex_preamble  = "\xf0\x00\x00\x0e\x22";
my $sysex_postamble = "\xf7";

sub build_sysex {
    my ($dump) = @_;
    my $checksum;
    {
        use integer;
        $checksum = -1 * (unpack '%32N*', $dump);
    }
    my $header = "Q01SYNTH" .                               # tag
                 pack('N',$checksum) .                      # checksum
                 "\x76\x31\x2e\x30\xff\xff\xff\xff" .       # version
                 ("\xff" x 12) .                            # date
                 ("\xff" x 12) .                            # time
                 pack('N',315) .                            # length
                 "\xff" .                                   # match_id
                 "\x00" .                                   # dirty
                 ("\xff" x 6);                              # padding

    return $sysex_preamble . pack('N',$global_sysex_opcode) . encode($header) . encode($dump) . $sysex_postamble;
}

# Translates a string from 7-bit chars to 8-bit chars.
sub decode {
    my $string = shift;
    my $decoded = '';
    my $chunk;
    # go through string by eight-byte chunks
    while (length($chunk = substr $string, 0, 8, '')) {
        # the first byte contains the high bits of the next seven bytes
        my ($highbits, @bytes) = unpack 'C8', $chunk;
        $decoded .= chr($_ | (($highbits <<= 1) & 0x80)) foreach @bytes;
    }
    return $decoded;
}

# Translates a string from 8-bit chars to 7-bit chars.
sub encode {
    my $string = shift;
    my $encoded = '';
    my $chunk;
    # go through string by seven-byte chunks
    while (length($chunk = substr $string, 0, 7, '')) {
        my $highbits = 0;
        my (@bytes) = unpack 'C7', $chunk;
        # rotate the high bit into $highbits and then clear it
        foreach (@bytes) {
            $highbits = ($highbits << 1) | ($_ >> 7);
            $_ &= 0x7f;
        }
        # output $highbits, followed by the seven 7-bit chars
        $encoded .= join '', map { chr } ($highbits, @bytes);
    }
    return $encoded;
}


#-----------------------------------------------------------------------------
#  Primary subroutines
#-----------------------------------------------------------------------------

my %options;
my $text;


sub txt_to_syx {
    my ($filename) = @_;
    $global_sysex_opcode = (1 << 24) + (4 << 16);   # edit buffer
    
    if ($options{l}) { $text = join '', @_; }
    else {
        open TXT, $filename or die qq(Could not open file "$filename": $!\n);
        $text = join '', <TXT>;
        close TXT;    
    }

    my $dump = chr(0) x 315;
    build_dump_from_txt(\$dump, $default_program_txt);
    build_dump_from_txt(\$dump, $text);
    my $syx = build_sysex($dump);
    if ($options{l}) { printf('%vx', $syx); }
    else {
        $filename =~ s!txt$!syx!i;
        open SYX, ">$filename" or die qq(Could not create file "$filename": $!\n);
        binmode SYX;
        print SYX $syx;
        close SYX;    
    }
    
    
}

sub syx_to_txt {
    my ($filename) = @_;

    open SYX, $filename or die qq(Could not open file "$filename".  $!\n);
    binmode SYX;
    local $/ = undef;
    my $sysex = <SYX>;
    close SYX;

    $sysex =~ s/\xf7$// or die qq("$filename" is not a valid sysex file.\n);
    my ($preamble, $opcode, $encoded_header, $encoded_content) = unpack "a5 N a64 a*", $sysex;
    my $content = decode($encoded_content);
    my $header = decode($encoded_header);

    if ($preamble ne $sysex_preamble or
        ($opcode >> 24) != 1 or
        substr($header, 0, 8) ne "Q01SYNTH") { die qq("$filename" is not an Ion/Micron program.\n); }
    if (($opcode & 0xffff) == 256) { die qq("$filename" is an Ion bank, not a single program.\n); }

    my $name = substr $content, 0, 14;
    $name =~ s/\x00//g;
    $name =~ s/[^\x20-\x7f]/ /g;

    my $source = is_program_from_micron($content) ? "Micron" : "Ion";
    if ($source eq 'Ion') {
        build_dump_from_txt(\$content, $ion_update_txt);
    }

    my $txt = banner_print("$source program:  $filename", "Generated on " . localtime);
    $txt =~ s/^\n+//;
    $txt =~ s/\n$//;

    $txt .= banner_print("Identification");
    $txt .= pretty_print("name", $name);
    $txt .= pretty_print("ion location", get_location_from_opcode($opcode));

    for my $param (@params) {
        my $category = $categories{$param->{name}};
        $txt .= banner_print($category) if defined $category;
        unless ($options{b}) {
            $txt .= "\n" unless defined $category;
            $txt .= verbose_print($param);
        }
        foreach_param($param, sub {
            my ($name, $offset) = @_;
            my $raw_value = read_param_from_dump($content, $offset, $param->{min}, $param->{max});
            my $formatted_value = get_formatted_value($param, $raw_value);
            $txt .= pretty_print($name, $formatted_value);
        });
    }

    $filename =~ s!syx$!txt!i;
    open TXT, ">$filename" or die qq(could not create file "$filename": $!\n);
    print TXT $txt;
    close TXT;
}


#-----------------------------------------------------------------------------
#  Main code
#-----------------------------------------------------------------------------

while ($ARGV[0] and $ARGV[0] =~ /^-(\w)/) { ++$options{$1}; shift }
my $filename = shift || usage();
if    ($filename =~ /\.syx$/i) { syx_to_txt($filename); }
elsif (($filename =~ /\.txt$/i) or ($options{l})) { txt_to_syx($filename); }
else                           { usage(); }
