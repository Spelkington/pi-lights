from src import LightStrip as ls
from src import PiMusic as pm
from src import config as cfg
from src import Palette as pal
import sys, termios, tty, os, time
import math



# Init setup
strip = ls.LightStrip(cfg.LED_COUNT)
audio = pm.PiMusic()

study_pal = pal.OCEAN
fun_pal   = pal.RAINBOW

try:

    strip.setPalette(study_pal)

    strip.setStepMode(strip.MODE_PALETTE)
    strip.setBrightness(1)

    counter = 0

    while True:

        audio.update()
        strip.step()

        strip.show()

except KeyboardInterrupt:
    strip.clear()
    strip.show()
    print("Stopping...")

# except Exception as e:
#     print(e)
#     strip.clear()
#     strip.show()
#     print("Stopping due to exception...")
