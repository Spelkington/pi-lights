import sys, os
sys.path.insert(0, os.path.abspath('..'))

from src import LightStrip as ls
from src import config as cfg
import math

strip = ls.LightStrip(cfg.LED_COUNT)

def generateSin(amplitude, period, speed, brightness):

    def sinwave(t):

        return [amplitude * math.sin(x*period / 1000 + t * speed / 1000) for x in cfg.LED_COUNT]

    return sinwave

try:

    redsin   = generateSin(10, 1, 0.1, 0)
    greensin = generateSin(20, 1.5, 0.5, 0)
    bluesin  = generateSin(30, 2, 0.25, 0)

    strip.loadChannelFunction(redSin, 0)
    strip.loadChannelFunction(greenSin, 1)
    strip.loadChannelFunction(blueSin, 2)

    while True:

        strip.stateStep()
        strip.show()

except KeyboardInterrupt:
    strip.clear()
    strip.show()
    print("Stopping...")
