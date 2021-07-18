import sys, os, getopt
sys.path.insert(0, os.path.abspath('..'))

from LightSphere import LightSphere
from Palette import Palette
import math
import time
import random as rand

def main():

    # Attempt to instantiate the lightstrip.
    sphere = LightSphere()
    sphere.setBrightness(0.4)

    palette = Palette([
        0xaa0000, #R
        0xaa6600, #O
        0xaaaa00, #Y
        0x00aa00, #G
        0x0000aa, #B
        0xaa00aa, #I
        0xaa0033, #V
        0xaa0000, #R
    ])

    # Instantiate the counter.
    NUM_SLICES = 32
    WAVELENGTH_ADJ = 0.2

    TOTAL_SPEED = 0.75

    WAVE_SPEED = 0.7
    AMPLITUDE_SPEED = 0.001

    LO_COLOR_SPEED = -0.1
    HI_COLOR_SPEED = -0.25

    MIN_AMPLITUDE = 60
    MAX_AMPLITUDE = 90

    raw_counter = 0
    try:

        sliceWidth = 360 / NUM_SLICES
        colorWidth = int(len(palette) / NUM_SLICES)

        while True:

            raw_counter += 1
            counter = int(raw_counter * TOTAL_SPEED)

            # Set the amplitude for the waveform
            amplitude = (MAX_AMPLITUDE - MIN_AMPLITUDE) * abs(math.sin(counter * AMPLITUDE_SPEED)) + MIN_AMPLITUDE

            for i in range(NUM_SLICES):

                thetaRange = (
                    i * sliceWidth,
                    (i + 1) * sliceWidth
                )

                loPhiRange = (
                    0,
                    90 + amplitude * math.sin((i + counter * WAVE_SPEED) * WAVELENGTH_ADJ)
                )

                hiPhiRange = (
                    90 + amplitude * math.sin((i + counter * WAVE_SPEED) * WAVELENGTH_ADJ),
                    180
                )

                loColorIndex = int((i + counter * LO_COLOR_SPEED) * colorWidth)
                hiColorIndex = int((i + counter * HI_COLOR_SPEED) * colorWidth)

                loColor = palette[loColorIndex % len(palette)]
                hiColor = palette[hiColorIndex % len(palette)]

                sphere[thetaRange:loPhiRange] = loColor
                sphere[thetaRange:hiPhiRange] = hiColor

            sphere.show()
            # sphere.clear()

    except KeyboardInterrupt:
        sphere.clear()
        sphere.show()
        print("Stopping...")

# Main entry
if __name__ == "__main__":
    main()
