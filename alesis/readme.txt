Ion/Micron Program Decoder v1.00          (c) 2004 Alesis Studio Electronics
August 19, 2004

WHAT THIS IS
------------
This is a command line utility to convert Ion and Micron programs from sysex
files to editable text files, and vice versa.  The utility runs under
Microsoft Windows, as well as on any operating system with Perl installed,
such as Mac OS X and most Linux installations.  Source code is included.

WHAT THIS IS NOT
----------------
This is not a "patch editor" or "sysex librarian".  It was designed to serve
as a backend for third parties interested in developing their own editors.
Think of it as a sysex specification in program form.  Although it is possible
to use this utility to edit programs by hand, Alesis cannot offer technical
support for enduser editing.

PACKAGE CONTENTS
----------------
This package contains the following files:

  readme.txt                : This file.
  ion_program_decoder.exe   : Windows executable.
  ion_program_decoder.pl    : Perl source code, and Mac/Linux executable.

INSTALLATION
------------
On Windows, no installation is required.  The program may be run by typing
its name at the command prompt.  Alternatively, you can drag-n-drop files
onto the program icon.

On Mac/Linux, you may need to set executable permissions for the script.
At the command line, type this:

  chmod 755 ion_program_decoder.pl

For Mac/Linux, substitute "ion_program_decoder.pl" for
"ion_program_decoder" in the command line examples below.

USAGE
-----
Send a program from the synth to your PC, and capture and save the sysex
file with a sequencer or MIDI utility.  To send a program from the Ion,
press [store], [page right], and [store] again.  To send a program from
the Micron, push the control knob, turn it right until you see
"Send MIDI sysex?" (third-to-last option), and push the control knob again.

Drag-n-drop the sysex file onto the ion_program_decoder.exe icon, or
type either of the following at the command line:

 ion_program_decoder my_program.syx
 ion_program_decoder -b my_program.syx

The utility will create a correspondingly-named text file (in this case,
named "my_program.txt").  This file lists all of the parameters of the
program.  The file normally documents all possible values for each
parameter as well.  For a briefer listing, use the -b option.

This text file may be edited directly.  To create a new sysex file from
the edited text file, drag-n-drop the text file onto the icon, or type
the following at the command line:

 ion_program_decoder my_program.txt

This will create "my_program.syx", overwriting it if it already exists.
The new sysex file can then be sent to the synth.  On the Ion, it will
be written to the bank/location indicated by the "ion location"
parameter.  On the Micron, if no program already exists with the same 
name, a new program will be created.  If a program does exist with the
same name, it will be overwritten, and any pattern, rhythms, and setups
that used the old program will use the new one.

