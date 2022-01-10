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
import neopixel
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

print(gc.mem_free())

green_to_off = (32768, 25600, 19456, 14336, 10240, 6912, 4352, 2560, 1280, 512, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

red_to_off = (8388608, 6553600, 4980736, 3670016, 2621440, 1769472, 1114112, 655360, 327680, 131072, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

pride = (8388608, 8388608, 8389376, 8391168, 8393984, 8398848, 8405248, 8414208, 6586368, 2654208, 688128, 32768, 22272, 8458, 1832, 100, 128, 131200, 589952, 1441920, 2555970, 3997718, 5963779, 8388608)

barbatos_pulse = (1544, 4889, 76343, 151140, 224909, 155510, 86370, 17489, 14657, 12083, 10795, 10535, 10274, 10015, 9755, 9496, 9239, 9239, 9239, 9239, 9239, 9239)

icy = (179, 65971, 658099, 1973939, 4342451, 8026803, 11776908, 11776806, 11776770, 9803008, 5592323, 2763280, 1052714, 197461, 149, 179, 329139, 1381811, 3355571, 6513587, 11053235, 11776947, 11776947, 11776947)

rgb = (8388608, 5701632, 3670784, 2165248, 1119744, 468992, 147968, 25600, 28928, 19457, 12293, 6925, 3355, 1328, 332, 113, 100, 131138, 458792, 1114134, 2162698, 3670019, 5701632, 8388608)

activeFader = Fader(pride)

while True:
    activeFader.update()
    dot[0] = activeFader.color
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
                    activeFader = Fader(green_to_off)
                elif val == "2":
                    activeFader = Fader(red_to_off)
                elif val == "3":
                    activeFader = Fader(pride)
                elif val == "4":
                    activeFader = Fader(barbatos_pulse)
                elif val == "5":
                    activeFader = Fader(icy)
                elif val == "6":
                    activeFader = Fader(rgb)
                print(val)
                
        except adafruit_irremote.IRNECRepeatException:  # unusual short code!
            print("NEC repeat!")
        except adafruit_irremote.IRDecodeException as e:     # failed to decode
            print("Failed to decode: ", e.args)
    print(gc.mem_free())
