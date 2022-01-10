# Circuit Playground Express Demo Code
# Adjust the pulseio 'board.PIN' if using something else
import gc

print(gc.mem_free())

import pulseio
import board
import adafruit_irremote

pulsein = pulseio.PulseIn(board.D2, maxlen=120, idle_state=True)
decoder = adafruit_irremote.GenericDecode()

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

while True:
    print("HERD")
    pulses = decoder.read_pulses(pulsein)
    print("Heard", len(pulses), "Pulses:", pulses)
    try:
        code = decoder.decode_bits(pulses)
        print("Decoded:", code)
        if len(code) > 3:
            command = code[2];
            print(codes[command])
    except adafruit_irremote.IRNECRepeatException:  # unusual short code!
        print("NEC repeat!")
    except adafruit_irremote.IRDecodeException as e:     # failed to decode
        print("Failed to decode: ", e.args)

    print("----------------------------")