from src import LightStrip as ls
from src import PiMusic as pm
from src import config as cfg
from src import Palette as pal
import math

strip = ls.LightStrip(cfg.LED_COUNT)
audio = pm.PiMusic()

try:

    palette = pal.TEST_PALETTE_TWO

    strip.setStepMode(strip.MODE_PALETTE)
    strip.setPalette(palette)

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
