# Trinket IO demo
# Welcome to CircuitPython 3.1.1 :)

import board
from digitalio import DigitalInOut, Direction, Pull
import touchio
import adafruit_dotstar as dotstar
import time
import neopixel
import gc
from fader import Fader, ModeFader, AutoOffFader

print(gc.mem_free())

writePixels = False;
logPixels = True;

# One pixel connected internally!
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=.1)

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
NUMPIXELS = 4
neopixels = neopixel.NeoPixel(board.D4, NUMPIXELS, brightness=0.2, auto_write=False)

print(gc.mem_free())

state = 'pride';
pride = (
        (16711680, 16711936, 16713216, 16716800, 16722688, 16732160, 16745216, 16762880, 13172480, 5308160, 1376000, 130816, 44801, 17172, 3664, 200, 255, 327935, 1179903, 2883839, 5111940, 8060972, 11927558, 16711680),
        (11730944, 11730944, 11731968, 11734528, 11738624, 11745280, 11754496, 11766784, 9220864, 3715840, 963328, 45824, 31232, 11790, 2616, 140, 179, 196787, 852147, 1966259, 3539036, 5636126, 8323076, 11730944),
        (8388608, 8388608, 8389376, 8391168, 8393984, 8398848, 8405248, 8414208, 6586368, 2654208, 688128, 32768, 22272, 8458, 1832, 100, 128, 131200, 589952, 1441920, 2555970, 3997718, 5963779, 8388608),
        (4980736, 4980736, 4981248, 4982272, 4984064, 4986880, 4990720, 4996096, 3951616, 1592320, 412672, 19456, 13312, 5126, 1048, 60, 76, 65612, 327756, 852044, 1507367, 2359309, 3538946, 4980736),
        (1638400, 1638400, 1638400, 1638912, 1639424, 1640448, 1641728, 1643520, 1317120, 530688, 137472, 6400, 4352, 1538, 264, 20, 25, 25, 65561, 262169, 458765, 786436, 1179648, 1638400),
        (786432, 786432, 786432, 786688, 786944, 787456, 787968, 788992, 658432, 265216, 68608, 3072, 2048, 769, 4, 10, 12, 12, 12, 131084, 196614, 393218, 589824, 786432),
)
prideFader = Fader(pride[0]);

def main():
  i = 0
  while True:
    prideFader.update();
    colorString = ''
    if(state == 'solid_green'):
      # spin internal LED around! autoshow is on
      dotColor = [0,255,0]
      if(writePixels):
        dot[0] = dotColor
      if(logPixels):
        colorString += getColorString(dotColor,' ')

      # also make the neopixels swirl around
      for p in range(NUMPIXELS):
          idx = int ((p * 256 / NUMPIXELS) + i)
          npColor = [0,255,0]
          if(writePixels):
            neopixels[p] = npColor
          if(logPixels):
            colorString += getColorString(npColor,' ')
      i = (i+1) % 256  # run from 0 to 255
      time.sleep(0.01) # make bigger to slow down
    elif(state == 'pride'):
      colorString += getColorString(unpack(prideFader.color), ' ')
      dot[0] = prideFader.color
    else:
      # spin internal LED around! autoshow is on
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

      i = (i+1) % 256  # run from 0 to 255
      time.sleep(0.01) # make bigger to slow down
    
    if(writePixels):
      neopixels.show()
    if(logPixels):
      print(colorString)

    # use D3 as capacitive touch to turn on internal LED
    if touch.value:
        print("D3 touched!")
    led.value = touch.value

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

def unpack(val):
  return [(val & 0xFF0000) >> 16, (val & 0x00FF00) >> 8, val & 0x0000FF]

main()