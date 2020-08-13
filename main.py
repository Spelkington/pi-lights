from lib import LightStrip as ls
import math

strip = ls.LightStrip(900)

def generateSinArrayFunction(a, b, c, d, e):

    def sinFunc(t):

        return [a * math.sin(b * x/5 + c+(t/e)) + d for x in range(len(strip))]

    return sinFunc

try:

    redSin = generateSinArrayFunction(100, 0.1, 0, 0, 10)
    greenSin = generateSinArrayFunction(15, 1, 0, 0, -10)

    strip.setChannelFunction(redSin, 0)
    strip.setChannelFunction(greenSin, 1)

    while True:

        strip.stateStep()
        strip.show()

except KeyboardInterrupt:
    strip.clear()
    strip.show()
    print("Stopping...")
