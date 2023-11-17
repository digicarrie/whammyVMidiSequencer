# whammyVMidiSequencer
A MIDI sequencer made for the Digitech Whammy V, made with a Raspberry Pico and CircuitPython. Uses an OLED ssd1306 display to print mode and subdivision information, 4 buttons to scroll up and down through modes and beat subdivisions, tap tempo to determine the average beat length, and a momentary switch to activate the sequence

# Functionality
- Mode selection (major chord, minor chord, etc)
- Beat subdivision selection (1/4, 1/3, etc)
- Tap Tempo
- Beat length averaging over 4 taps

# Wiring
OLED sda: GP0
OLED scl: GP1
Mode left btn: GP2
Mode right btn: GP3
Subdivison left btn: GP4
Subdivision right btn: GP5
Tap Tempo btn: GP6
Seqence start btn: GP7
MIDI tx: GP8
MIDI rx (unused but defined): GP9

The second half of every button goes to the 5v Vbus of the Pico
