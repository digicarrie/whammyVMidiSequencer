import board
import keypad
import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import adafruit_ssd1306
import digitalio
import time
from digitalio import DigitalInOut, Direction, Pull
import adafruit_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.program_change import ProgramChange


displayio.release_displays()

i2c = busio.I2C(board.GP1, board.GP0)  # uses board.SCL and board.SDA
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# Make the display context
splash = displayio.Group()
display.show(splash)


mode = ["DryMajUp","DryMajDown", "DryMajUp","DryMajDown",
        "DryMinUp","DryMinDown", "DryMinUp","DryMinDown",
        "DryMaj7", "DryMaj7",
        "WhamFifth", "WhamFifth",
        "WhamMajUp", "WhamMajDown", "WhamMajUp", "WhamMajDown"
        "WhamMinUp", "WhamMinDown", "WhamMinUp", "WhamMinDown"
        "WhamMaj7", "WhamMaj7",        
        "Oct Up", "Oct Down"]
modeIndex = 0
modeNumber = [3, 3, 4, 4, 3, 3, 4, 4, 3, 4, 3, 4, 3, 3, 4, 4, 3, 3, 4, 4, 3, 4, 2, 2] 
sub = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64]
subIndex = 3
        
trueTime = [200,201]
timeBits = [0.5,0.5,0.5,0.5]
beatLength = 0.5
wait = 0.5


text_areaMode = label.Label(terminalio.FONT, text="mode:", scale=1, color=0xFFFF00, x=0, y=5)			# printing the main mode label
text_areaSub = label.Label(terminalio.FONT, text="subdivision:", scale=1, color=0xFFFF00, x=0, y=37)	# printing the main subdivision label
splash.append(text_areaMode)
splash.append(text_areaSub)


                                                                            # the following buttons are keypads for debouncing purposes
tapTempo = keypad.Keys((board.GP6,), value_when_pressed=True, pull=True)	# making the tap tempo button
btnModeLeft = keypad.Keys((board.GP2,) value_when_pressed=True, pull=True)	# mode left button
btnModeRight = keypad.Keys((board.GP3,) value_when_pressed=True, pull=True)	# mode right button
btnSubLeft = keypad.Keys((board.GP4,) value_when_pressed=True, pull=True)	# sub left button
btnSubRight = keypad.Keys((board.GP5,) value_when_pressed=True, pull=True)	# sub right button

btnStart = digitalio.DigitalInOut(board.GP7)				# button for main sequencer start
btnStart.switch_to_input(pull=digitalio.Pull.DOWN)			# this is not a keypad as there should not be debouncing on this button

text_areaModeNumber = label.Label(terminalio.FONT, text=modeNumber[modeIndex], scale=1, color=0xffff00, x=0, y=20)	# creating the label for the number of notes
text_areaModeLabel = label.Label(terminalio.FONT, text=mode[modeIndex], scale=2, color=0xFFFF00, x=5, y=20)			# creating the label for the mode name
text_areaSubLabel = label.Label(terminalio.FONT, text="1/"+str(sub[subIndex]), scale=2, color=0xFFFF00, x=0, y=52)	# creating the label for the subdivison type
splash.append(text_areaModeNumber)
splash.append(text_areaModeLabel)
splash.append(text_areaSubLabel)

uart = busio.UART(tx=board.GP8, rx=board.GP9, baudrate=31250, timeout=0.001)  # init UART
midi_in_channel = 2
midi_out_channel = 1
midi = adafruit_midi.MIDI(
    midi_in=uart,
    midi_out=uart,
    in_channel=(midi_in_channel - 1),
    out_channel=(midi_out_channel - 1),
    debug=True,
)

def updateModeDisplay():		# instead of clearing the display, this changes the the color of the text to black, then updates the text, then
    global text_areaModeLabel		# changes the color back to white
    text_areaModeLabel.color=0x000000
    text_areaModeNumber.color=0x000000
    text_areaModeLabel.text = mode[modeIndex]
    text_areaModeNumber.text = modeNumber[modeIndex]
    text_areaModeLabel.color=0xffff00
    text_areaModeNumber.color=0xffff00
def updateSubDisplay():
    global text_areaSubLabel
    text_areaSubLabel.color=0x000000
    text_areaSubLabel.text = "1/"+str(sub[subIndex])
    text_areaSubLabel.color=0xffff00
    
def play():
    wait = beatLength / sub[subIndex]
    if modeIndex == 0:
        harmMaj3rd(); time.sleep(wait); harm5th(); time.sleep(wait); harmOctUp(); time.sleep(wait);
    elif modeIndex == 1:
        harmOctUp(); time.sleep(wait); harm5th(); time.sleep(wait); harmMaj3rd(); time.sleep(wait);
    elif modeIndex == 2:
        harmMaj3rd(); time.sleep(wait); harm5th(); time.sleep(wait); harmOctUp(); time.sleep(wait); harm5th(); time.sleep(wait);
    elif modeIndex == 3:
        harmOctUp(); time.sleep(wait); harm5th(); time.sleep(wait); harmMaj3rd(); time.sleep(wait); harm5th(); time.sleep(wait);
    elif modeIndex == 4:
        harmMin3rd(); time.sleep(wait); harm5th(); time.sleep(wait); harmOctUp(); time.sleep(wait);
    elif modeIndex == 5:
        harmOctUp(); time.sleep(wait); harm5th(); time.sleep(wait); harmMin3rd(); time.sleep(wait);
    elif modeIndex == 6:
        harmMin3rd(); time.sleep(wait); harm5th(); time.sleep(wait); harmOctUp(); time.sleep(wait); harm5th(); time.sleep(wait);
    elif modeIndex == 7:
        harmOctUp(); time.sleep(wait); harm5th(); time.sleep(wait); harmMin3rd(); time.sleep(wait); harm5th(); time.sleep(wait);
    elif modeIndex == 8:
        harmMaj3rd(); time.sleep(wait); harm5th(); time.sleep(wait); harm7th(); time.sleep(wait);
    elif modeIndex == 9:
        harmMaj3rd(); time.sleep(wait); harm5th(); time.sleep(wait); harm7th(); time.sleep(wait); harm5th(); time.sleep(wait);
    elif modeIndex == 10:
        harmOctUp(); time.sleep(wait); harm5th(); time.sleep(wait); harm5thDown(); time.sleep(wait);
    elif modeIndex == 11:
        harmOctUp(); time.sleep(wait); harm5th(); time.sleep(wait); harm5thDown(); time.sleep(wait); harm5th();
    elif modeIndex == 12:
        octUp(); time.sleep(wait); bypass(); time.sleep(wait);
    elif modeIndex == 13:
        octDown(); time.sleep(wait); bypass(); time.sleep(wait);
        
def toeDown():						# Toe Down
  midi.send(ControlChange(11, 126))
def toeUp():						# Toe up
  midi.send(ControlChange(11, 0))
def bypass():						# whammy 1 octave with toe up
  midi.send(ProgramChange(43))
  toeUp()
def harmOctUp():					# harmony mode, oct up
  midi.send(ProgramChange(62))
  toeDown()
def harmOctDown():					# harmony mode, oct down
  midi.send(ProgramChange(62))
  toeUp()
def harmMaj3rd():					# harmony mode, maj 3rd		
  midi.send(ProgramChange(55))
  toeDown()
def harmMin3rd():					# harmony mode, min 3rd
  midi.send(ProgramChange(55))
  toeUp()
def harm5th():						# harmony mode, 5th
  midi.send(ProgramChange(57))
  toeDown()
def harm5thDown():					# harmony mode, 5th down
  midi.send(ProgramChange(61))
  toeUp()
def harm7th():						# harmony mode, 7th
  midi.send(ProgramChange(59))
  toeDown()
def octUp():							# whammy 1 oct up
  midi.send(ProgramChange(43))
  toeDown()
def octDown():						# whammy 1 oct down
  midi.send(ProgramChange(49))
  toeDown()
def wham5th():						# whammy 5th up
  midi.send(ProgramChange(44))
  toeDown()
def wham4th():						# whammy 4th up
  midi.send(ProgramChange(45))
  toeDown()
        

while True:
    tapTempoEvent = tapTempo.events.get()			# making objects that contain the button event information
    btnModeLeftEvent = btnModeLeft.events.get()			# potential data leak? time will tell
    btnModeRightEvent = btnModeRight.events.get()
    btnSubLeftEvent = btnSubLeft.event.get()
    btnSubRightEvent = btnSubRight.event.get()
    if tapTempoEvent.pressed:
        print(event)
        trueTime[0] = trueTime[1]			# shuffling the true time value
        trueTime[1] = time.monotonic()		# getting new true time value
        timeBits[0] = timeBits[1]			# shuffling the beat time history
        timeBits[1] = timeBits[2]
        timeBits[2] = timeBits[3]
        if trueTime[1]-trueTime[0] > 3:		# if the beat length is greater than 3s, fill with an earlier smaller value
            timeBits[3] = timeBits[0]		# this is because if you do not press the tap tempo for a while, the next timeBits value will be very very high, and
        else:								# distort the average beat length
            timeBits[3] = trueTime[1] - trueTime[0]
            beatLength = sum(timeBits)/4
            print(beatLength)
    
    if btnModeLeftEvent.pressed and modeIndex >= 1:
        modeIndex +=-1
        updateModeDisplay()   
    if btnModeRightEvent.pressed and modeIndex < len(mode):
        modeIndex +=1
        updateModeDisplay()
    if btnSubLeftEvent.pressed and subIndex >= 1:
        subIndex += -1
        updateSubDisplay()
    if btnSubRightEvent.pressed and subIndex < len(sub):
        subIndex += 1
        updateSubDisplay()
    if btnStart.value:
        play()
        bypass()
    pass

