# Circuit Playground Express Demo Code
# Adjust the pulseio 'board.PIN' if using something else
import gc

print(gc.mem_free())

import pulseio
import board
import adafruit_irremote
from digitalio import DigitalInOut, Direction, Pull
import adafruit_dotstar as dotstar
import time
#import neopixel
from fader import Fader, ModeFader, AutoOffFader


pulsein = pulseio.PulseIn(board.D2, maxlen=120, idle_state=True)
decoder = adafruit_irremote.GenericDecode()
# One pixel connected internally!
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=.1)


# IR Remote Mapping
'''
 1: [255, 2, 247, 8]
 2: [255, 2, 119, 136]
 3: [255, 2, 183, 72]
 4: [255, 2, 215, 40]
 5: [255, 2, 87, 168]
 6: [255, 2, 151, 104]
 7: [255, 2, 231, 24]
 8: [255, 2, 103, 152]
 9: [255, 2, 167, 88]
 0: [255, 2, 207, 48]

^ : [255, 2, 95, 160]
v : [255, 2, 79, 176]
> : [255, 2, 175, 80]
< : [255, 2, 239, 16]

Enter: [255, 2, 111, 144]
Setup: [255, 2, 223, 32]
Stop/Mode: [255, 2, 159, 96]
Back: [255, 2, 143, 112]

Vol - : [255, 2, 255, 0]
Vol + : [255, 2, 191, 64]

Play/Pause: [255, 2, 127, 128]
'''
codes = {
    247:"1",
    119:"2",
    183:"3",
    215:"4",
    87:"5",
    151:"6",
    231:"7",
    103:"8",
    167:"9",
    207:"0",
    95:"^",
    79:"v",
    175:">",
    239:"<",
    111:"Enter",
    223:"Setup",
    159:"Stop/Mode",
    143:"Back",
    255:"Vol -",
    191:"Vol +",
    127:"Play/Pause"
};

gamma = (
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
   10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
   17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
   25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
   37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
   51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
   69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
   90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
  115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
  144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
  177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
  215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255 )

print(gc.mem_free())

green_to_off = (65280, 59648, 54016, 48384, 42496, 36864, 31232, 25600, 19712, 14080, 8448, 2816, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

red_to_off = (16711680, 15269888, 13828096, 12386304, 10878976, 9437184, 7995392, 6553600, 5046272, 3604480, 2162688, 720896, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

pride = (16711680, 16720128, 16728576, 16737024, 16745728, 16754176, 16762880, 16771328, 15335168, 10944256, 6618880, 2227968, 56865, 39780, 22950, 5865, 1573119, 3932415, 6357247, 8716543, 10748104, 12779653, 14745666, 16711680)

barbatos_pulse = (0, 664873, 1395538, 2126204, 2856613, 3587278, 3921386, 3263195, 2604749, 1946558, 1288112, 629921, 365975, 431249, 496523, 561541, 626815, 691833, 757368, 757368, 757368, 757368, 757368, 757368)

icy = (255, 2895103, 5789951, 8750591, 11645439, 14606079, 16777193, 16777104, 16777015, 15724304, 12763708, 9803113, 6908309, 3947714, 1052911, 1776639, 4737279, 7632127, 10592767, 13487615, 16448255, 16777215, 16777215, 16777215)

rgb = (16711680, 14557440, 12403200, 10183680, 8029440, 5875200, 3655680, 1501440, 62475, 54060, 45645, 36975, 28560, 19890, 11475, 3060, 1442025, 3604680, 5832870, 7995525, 10158180, 12386370, 14549025, 16711680)

activeFader = Fader(pride)
activeInterval = 0.1
brightnessModifier = 0;

def gammaCorrect(val, brightnessModifier=0):
    rgb_val = unpack(val);
    r = min(255, max(0, rgb_val[0] + brightnessModifier))
    g = min(255, max(0, rgb_val[1] + brightnessModifier))
    b = min(255, max(0, rgb_val[2] + brightnessModifier))
    return [gamma[r],gamma[g],gamma[b]]

def unpack(val):
  return [(val & 0xFF0000) >> 16, (val & 0x00FF00) >> 8, val & 0x0000FF]

while True:
    activeFader.update()
    dot[0] = gammaCorrect(activeFader.color, brightnessModifier)
    pulses = decoder.read_pulses(pulsein, blocking=False, pulse_window=0.01, blocking_delay=0.01)
    if(pulses != None):
        #print("Heard", len(pulses), "Pulses:", pulses)
        try:
            code = decoder.decode_bits(pulses)
            #print(code)
            #print("Decoded:", code)
            if code != None and len(code) > 3:
                command = code[2];
                val = codes[command];
                if val == "1":
                    activeFader = Fader(green_to_off, interval=activeInterval)
                elif val == "2":
                    activeFader = Fader(red_to_off, interval=activeInterval)
                elif val == "3":
                    activeFader = Fader(pride, interval=activeInterval)
                elif val == "4":
                    activeFader = Fader(barbatos_pulse, interval=activeInterval)
                elif val == "5":
                    activeFader = Fader(icy, interval=activeInterval)
                elif val == "6":
                    activeFader = Fader(rgb, interval=activeInterval)
                elif val == "<":
                    activeInterval += 0.02
                    activeFader.interval = activeInterval;
                elif val == ">":
                    activeInterval = max(0.01, activeInterval - 0.02);
                    activeFader.interval = activeInterval;
                elif val == "^":
                    brightnessModifier += 5;
                elif val == "v":
                    brightnessModifier -= 5;
                print(val)
                
        except adafruit_irremote.IRNECRepeatException:  # unusual short code!
            print("NEC repeat!")
        except adafruit_irremote.IRDecodeException as e:     # failed to decode
            print("Failed to decode: ", e.args)
    print(gc.mem_free())
