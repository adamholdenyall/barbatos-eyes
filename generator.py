#gradient generator from https://jjmojojjmojo.github.io/time-based-fading.html

import adafruit_fancyled as fancy
from fader import Fader
import time

DIM_LEVELS = (2.0, 1.0, 0.7, 0.5, 0.3, 0.1, 0.05)
COLORS = 24

WHITE = fancy.CRGB(255, 255, 255)
BLACK = fancy.CRGB(0, 0, 0)
GRAY = fancy.CRGB(127, 127, 127)
RED = fancy.CRGB(255, 0, 0)
GREEN = fancy.CRGB(0, 255, 0)
YELLOW = fancy.CRGB(255, 255, 0)
BLUE = fancy.CRGB(0, 0, 255)
ORANGE = fancy.CRGB(255, 127, 0)
VIOLET = fancy.CRGB(139, 0, 255)
INDIGO = fancy.CRGB(46, 43, 95)

PINK = fancy.CRGB(255, 127, 127)
MINT = fancy.CRGB(127, 255, 127)
ROBIN = fancy.CRGB(127, 127, 255)

def make_gradient(colors, steps=24, brightness=0.1, wrap=True):
    values = []
    ratio = 1.0/len(colors)
    for index, color in enumerate(colors):
        value = float(index*ratio)
        values.append((value, color))

    if wrap:
        values.append((1.0, colors[0]))

    palette = []
    for expanded in fancy.expand_gradient(values, steps):
        if(brightness <= 1.0):
            palette.append(fancy.gamma_adjust(expanded, brightness=brightness).pack())
        else:
            palette.append(expanded.pack())

    return tuple(palette)

gradients = {
    'pride': ([RED,ORANGE,YELLOW,GREEN,BLUE,VIOLET], True),
    'halloween': ([ORANGE,VIOLET], True),
    'anna_howard_shaw': ([RED,WHITE,PINK,WHITE], True),
    'pastels': ([PINK,WHITE,MINT,WHITE,ROBIN,WHITE], True),
    'rgb': ([RED, GREEN, BLUE], True),
    'july4': ([RED, WHITE, WHITE, BLUE], True),
    'ireland': ([GREEN, WHITE, ORANGE], True),
    'icy': ([BLUE, ROBIN, WHITE, YELLOW, GRAY, BLUE, ROBIN, WHITE], False),
    'gray': ([WHITE, GRAY, BLACK, GRAY, WHITE], True),
    'white_to_off': ([WHITE, BLACK], False),
    'green_to_off': ([GREEN, BLACK], False),
    'blue_to_off': ([BLUE, BLACK], False),
    'red_to_off': ([RED, BLACK], False),
}

def generate():
    while True:
        for name, data in gradients.items():
            colors, wrap = data
            for brightness in DIM_LEVELS:
                yield make_gradient(colors, COLORS, brightness, wrap)

cycler = generate()

for name, data in gradients.items():
    colors, wrap = data
    print(name, "= (")
    for brightness in DIM_LEVELS:
        gradient = make_gradient(colors, COLORS, brightness, wrap)
        print("\t", gradient, ",", sep="")
    print(")")

checkin = time.monotonic()
previous = 0