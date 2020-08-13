from lib import LightStrip as ls
import math

strip = ls.LightStrip(900)

try:

    t = 0
    while True:

        brightness = 128 * math.sin(t/50)
        
        strip.clear()
        strip[t % 4:len(strip):4] = (0, 0, brightness)
        strip.show()

        t += 1

except KeyboardInterrupt:
    strip.clear()
    strip.show()
    print("Stopping...")
