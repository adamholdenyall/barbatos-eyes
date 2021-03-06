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
barbatos_pulse = (
        (0, 664873, 1395538, 2126204, 2856613, 3587278, 3921386, 3263195, 2604749, 1946558, 1288112, 629921, 365975, 431249, 496523, 561541, 626815, 691833, 757368, 757368, 757368, 757368, 757368, 757368),
        (0, 257, 2316, 7204, 146766, 225424, 368073, 231337, 95117, 25203, 20829, 17226, 15422, 14903, 14641, 14124, 13863, 13602, 13345, 13345, 13345, 13345, 13345, 13345),
        (0, 257, 1544, 4889, 76343, 151140, 224909, 155510, 86370, 17489, 14657, 12083, 10795, 10535, 10274, 10015, 9755, 9496, 9239, 9239, 9239, 9239, 9239, 9239),
        (0, 0, 1030, 3602, 73255, 79944, 151140, 82772, 14662, 12601, 10286, 8485, 7711, 7451, 7192, 6934, 6931, 6673, 6672, 6672, 6672, 6672, 6672, 6672),
        (0, 0, 515, 2058, 4631, 74027, 77628, 10290, 8746, 7458, 6172, 5142, 4626, 4368, 4366, 4109, 4107, 3850, 3850, 3850, 3850, 3850, 3850, 3850),
        (0, 0, 1, 515, 1543, 2830, 3860, 3344, 2830, 2315, 2057, 1543, 1542, 1285, 1284, 1284, 1283, 1283, 1283, 1283, 1283, 1283, 1283, 1283),
        (0, 0, 0, 257, 771, 1287, 1802, 1544, 1287, 1029, 1028, 771, 771, 514, 514, 514, 513, 513, 513, 513, 513, 513, 513, 513),
)
prideFader = Fader(barbatos_pulse[0]);

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