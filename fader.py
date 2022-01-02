#Adapted from Fader class from https://jjmojojjmojo.github.io/time-based-fading.html

import time

class Fader:
    def __init__(self, palette, interval=0.1):
        self.checkin = time.monotonic()
        self.color = 0
        self.interval = interval
        self.palette = palette
        self.max = len(self.palette)*interval
        self.epoch = 0
        self.index = 0

    def update(self):
        self.epoch = time.monotonic() - self.checkin

        self.index = round((self.epoch%self.max)/self.interval)

        if self.index > len(self.palette)-1:
            self.index = 0
            self.checkin = time.monotonic()

        self.color = self.palette[self.index]

class ModeFader(Fader):
    def __init__(self, palette, interval=0.1):
        self.on = True
        Fader.__init__(self, palette, interval)

    def update(self):
        if not self.on:
            self.color = 0
            return

        Fader.update(self)

class AutoOffFader(ModeFader):
    def reset(self):
        self.epoc = 0
        self.checkin = time.monotonic()
        self.on = True
        self.index = 0

    def update(self):
        ModeFader.update(self)
        if self.on and self.index == len(self.palette)-1:
            self.on = False