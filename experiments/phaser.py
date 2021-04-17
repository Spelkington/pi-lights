import sys, os
sys.path.insert(0, os.path.abspath('..'))

from src import LightStrip as ls
from src import config as cfg
import math

strip = ls.LightStrip(cfg.LED_COUNT)

# Linear interpolation from a to b, t: [0, 1] where t=0 returns a and t=1 returns b.
def mix(a, b, t):
    # TODO: Linear interpolation
    pass

class Pulse:
    def __init__(self, radius, color, speed):
        self.radius = radius
        self.color = color
    
    # Moves the pulse forward in time
    def step(self, dt):
        # TODO apply the pulse to the array
        pass
        
    # Paints the pulse onto the array, using additive blending
    def apply(self, array):
        # TODO apply the pulse to the array
        pass

def Phaser:
    def __init__(self, rate, palette):
        self.rate = rate
        self.palette = palette 
        self.pulses = []

    def apply(self, array):
        for pulse in self.pulses:
            pulse.apply(array)

    def step(self, dt):
        # TODO start new pulses
        for pulse in self.pulses:
            pulse.step(dt)
        # TODO kill pulses that have gone off the end

try:
    phaser = Phaser(2, [])

    while True:
        # TODO: The way we do additive blending assumes the strip is all 0s
        phaser.step(1/60)
        phaser.apply(strip)
        strip.show()
    print(len(strip))

except KeyboardInterrupt:
    strip.clear()
    strip.show()
    print("Stopping...")
