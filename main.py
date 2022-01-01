# Trinket IO demo
# Welcome to CircuitPython 3.1.1 :)

import board
from digitalio import DigitalInOut, Direction, Pull
import touchio
import adafruit_dotstar as dotstar
import time
import neopixel

writePixels = False;
logPixels = True;

# One pixel connected internally!
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Digital input with pullup on D2
button = DigitalInOut(board.D2)
button.direction = Direction.INPUT
button.pull = Pull.UP

# Capacitive touch on D3
touch = touchio.TouchIn(board.D3)

# NeoPixel strip (of 16 LEDs) connected on D4
NUMPIXELS = 16
neopixels = neopixel.NeoPixel(board.D4, NUMPIXELS, brightness=0.2, auto_write=False)

######################### HELPERS ##############################

# Helper to give us a nice color swirl
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0):
        return (0, 0, 0)
    if (pos > 255):
        return (0, 0, 0)
    if (pos < 85):
        return (int(pos * 3), int(255 - (pos*3)), 0)
    elif (pos < 170):
        pos -= 85
        return (int(255 - pos*3), 0, int(pos*3))
    else:
        pos -= 170
        return (0, int(pos*3), int(255 - pos*3))

def getColorString(color,text):
    return ('\033[1;48;2;'+str(color[0])+';'+str(color[1])+';'+str(color[2])+'m'+text+'\033[0m');
        
######################### MAIN LOOP ##############################

i = 0
while True:
  # spin internal LED around! autoshow is on
  colorString = ''
  dotColor = wheel(i & 255)
  if(writePixels):
    dot[0] = dotColor
  if(logPixels):
    colorString += getColorString(dotColor,' ')

  # also make the neopixels swirl around
  for p in range(NUMPIXELS):
      idx = int ((p * 256 / NUMPIXELS) + i)
      npColor = wheel(idx & 255)
      if(writePixels):
        neopixels[p] = npColor
      if(logPixels):
        colorString += getColorString(npColor,' ')
  if(writePixels):
    neopixels.show()
  if(logPixels):
    print(colorString)
  
  # use D3 as capacitive touch to turn on internal LED
  if touch.value:
      print("D3 touched!")
  led.value = touch.value

  i = (i+1) % 256  # run from 0 to 255
  time.sleep(0.01) # make bigger to slow down