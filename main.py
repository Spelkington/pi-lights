from src import LightStrip as ls
from src import PiMusic as pm
from src import config as cfg
from src import Palette as pal
import sys, termios, tty, os, time
import math

def sinFunction(amp, per, vel, shift, prev=None):

    def sinFunc(x, t):

        result = amp * math.sin(x * per/100 + t * vel/100) + shift

        if prev:
            return result + prev(x, t)
        else:
            return result

    return sinFunc

def sinChannel(sinFunc):

    def channelFunc(t):
        return [int(sinFunc(x, t)) for x in range(cfg.LED_COUNT)]

    return channelFunc

strip = ls.LightStrip(cfg.LED_COUNT)
audio = pm.PiMusic()

try:

    sinFunc = sinFunction(75, 10, 5, 64)
    sinFunc = sinFunction(100, 0.05, -2, 40, sinFunc)
    sinFunc = sinChannel(sinFunc)

    palettes = (
            pal.RAINBOW,
            pal.OCEAN,
            pal.FOREST,
    )
    paletteIndex = 1

    strip.setChannelFunction(sinFunc, strip.CH_PALETTE)

    strip.setStepMode(strip.MODE_PALETTE)
    strip.setPalette(palettes[paletteIndex])
    strip.setBrightness(32)

    counter = 0

    while True:

        counter += 1
        if counter % 1000 == 0:
            print("Palette changed!")
            paletteIndex = (paletteIndex + 1) % len(palettes)
            strip.setPalette(palettes[paletteIndex])

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
