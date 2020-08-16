from src import LightStrip as ls
from src import PiMusic as pm
from src import config as cfg
import math

strip = ls.LightStrip(cfg.LED_COUNT)
audio = pm.PiMusic()

try:

    audio.printDevices()

    while True:

        audio.update()
        strip.stateStep()
        strip.show()

except KeyboardInterrupt:
    strip.clear()
    strip.show()
    print("Stopping...")
