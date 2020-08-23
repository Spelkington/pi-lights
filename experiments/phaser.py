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
        
    # Paiints the pulse onto the array, using additive blending
    def apply(self, array):
        # TODO apply the pulse to the array
        pass

try:
    print(len(strip))

except KeyboardInterrupt:
    strip.clear()
    strip.show()
    print("Stopping...")
