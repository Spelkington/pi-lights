import time
import math
import random
import noise
import numpy as np
from rpi_ws281x import *

LED_COUNT       = 900
LED_PIN         = 18
LED_FREQ_HZ     = 800000
LED_DMA         = 10
LED_BRIGHTNESS  = 255
LED_INVERT      = False
LED_CHANNEL     = 0


def fill(strip, color):
    for i in range(LED_COUNT):
        strip.setPixelColor(i, color)

def getColorValues(color):
    r = (color & 0xff0000) >> 16
    g = (color & 0x00ff00) >> 8
    b = (color & 0x0000ff) >> 0

    return [r, g, b]

def applyColorArrayToStrip(strip, array, channel, weight = 1):

    for i in range(min(LED_COUNT, len(array))):
        newColor = getColorValues(strip.getPixelColor(i))

        newColor[channel] = max(0, min(int(array[i] * 255 * weight), 255))
        newColor = Color(newColor[0], newColor[1], newColor[2])

        strip.setPixelColor(i, newColor)

if __name__ == '__main__':

    strip = Adafruit_NeoPixel(  
                                LED_COUNT,
                                LED_PIN,
                                LED_FREQ_HZ,
                                LED_DMA,
                                LED_INVERT,
                                LED_BRIGHTNESS,
                                LED_CHANNEL
                             )

    strip.begin()

    colorShape = (LED_COUNT * 3, 1000)
    colorScale = 100.0
    colorOctaves = 6
    colorPersistence = 0.5
    colorLacunarity = 2.0

    colorWeights = [1, 1, 1]

    print("Generating Perlin Noise Pattern...")

    colorPattern = np.zeros(colorShape)
    for i in range(colorShape[0]):
        for j in range(colorShape[1]):
            colorPattern[i][j] = noise.pnoise2(i/colorScale,
                                          j/colorScale,
                                          octaves=colorOctaves,
                                          persistence=colorPersistence,
                                          lacunarity=colorLacunarity,
                                          repeatx=colorShape[0],
                                          repeaty=colorShape[1],
                                          base=0)

    brightnessShape = (1, 1000)
    brightnessScale = 100.0
    brightnessOctaves = 6
    brightnessPersistence = 0.5
    brightnessLacunarity = 2.0

    brightnessPattern = np.zeros(brightnessShape)
    for i in range(brightnessShape[0]):
        for j in range(brightnessShape[1]):
            brightnessPattern[i][j] = noise.pnoise2(i/brightnessScale,
                                          j/brightnessScale,
                                          octaves=brightnessOctaves,
                                          persistence=brightnessPersistence,
                                          lacunarity=brightnessLacunarity,
                                          repeatx=brightnessShape[0],
                                          repeaty=brightnessShape[1],
                                          base=0)


    try:

        t = 0
        t_step = 1

        while True:

            t += t_step
            t = t % LED_COUNT

            for i in range(3):
                applyColorArrayToStrip(strip, colorPattern[t + i*LED_COUNT], i, colorWeights[i])

            brightness = int(brightnessPattern[0][t] * 255) + 60
            brightness = max(0, min(255, brightness))
            strip.setBrightness(brightness)

            strip.show()

    except KeyboardInterrupt:
        print("stopping...")
        fill(strip, Color(0, 0, 0))
        strip.show()

