import sys, os, getopt
sys.path.insert(0, os.path.abspath('..'))

import math
import yaml
import random as rand
from src import LightStrip as ls
from src import Palette as pal
from src import config as cfg
from datetime import datetime

def generateSin(amplitude, period, speed, center):

    def sinwave(t):

        return [amplitude * math.sin(x*period / 1000 + t * speed / 1000) + center for x in range(cfg.LED_COUNT)]

    return sinwave

def combineFuncs(funcs):

    def combined(t):

        result = [0 for _ in range(cfg.LED_COUNT)]

        for func in funcs:
            layer = func(t)
            result = [result[i] + layer[i] for i in range(cfg.LED_COUNT)]

        return result

    return combined

def createWaveFunction(ranges, speedMult = 1, verbose = False):

    funcs = []

    for key, r in ranges.items():

        kwargs = {
            "amplitude": rand.random() * (r["amp"]["max"] - r["amp"]["min"]) + r["amp"]["min"],
            "period":    rand.random() * (r["period"]["max"] - r["period"]["min"]) + r["period"]["min"],
            "speed":    (rand.random() * (r["speed"]["max"] - r["speed"]["min"]) + r["speed"]["min"]) * speedMult,
            "center":    rand.random() * (r["center"]["max"] - r["center"]["min"]) + r["center"]["min"],
        }

        if verbose:
            print(key.upper())
            for kwname, kwval in kwargs.items():
                print("\t", kwname, kwval)
            print()

        funcs.append(generateSin(**kwargs))

    return combineFuncs(funcs)

def updateParams(strip, CONFIG, hotswap=False):

    if hotswap:
        with open(r'config.yaml') as file:
            CONFIG = yaml.load(file, Loader=yaml.FullLoader)
            print("CONFIG Hot-swapped!")

            for name, colors in CONFIG["palettes"].items():
                CONFIG["palettes"][name] = pal.generatePalette(colors)

    # Convert all config palettes to real palettes
    for name, colors in CONFIG["palettes"].items():
        CONFIG["palettes"][name] = pal.generatePalette(colors)

    # Define study and break palettes
    studyPals = CONFIG["study-palettes"]
    breakPals = CONFIG["break-palettes"]

    studyPal = studyPals[rand.randint(0, len(studyPals) - 1)]
    breakPal = breakPals[rand.randint(0, len(breakPals) - 1)]

    if CONFIG["verbose"] == True:
        print("Study: ", studyPal)
        print("Break: ", breakPal)

    if CONFIG["verbose"] == True:
        print("Study Speed: ", CONFIG["study-speed"])
        print("Break Speed: ", CONFIG["break-speed"])

    studyPal = CONFIG["palettes"][studyPal]
    breakPal = CONFIG["palettes"][breakPal]

    now = datetime.now()
    studyOn = (
            now.minute < CONFIG["swap-minute"]
        and now.hour < CONFIG["last-hour"]
        and not now.day in CONFIG["break-days"]
        and not CONFIG["no-change"]
    )

    # Because the timelevel formula has an asymptote at 12,
    # a conditional is required to close the gap.
    if now.hour != CONFIG["peak-hour"]:
        timeLevel = min(1, (8 / (now.hour - CONFIG["peak-hour"])**2))
    else:
        timeLevel = 1

    studySpeed = CONFIG["study-speed"] * timeLevel
    breakSpeed = CONFIG["break-speed"] * timeLevel
    brightness = min(
        CONFIG["brightness-max"], 
        CONFIG["brightness-mult"] * timeLevel
    )

    strip.setBrightness(brightness)
    waveform = CONFIG["waveforms"][CONFIG["loaded-waveform"]]

    if studyOn:

        if CONFIG["verbose"] == True:
            print("Mode: Study")

        strip.setPalette(studyPal)
        strip.setChannelFunction(createWaveFunction(
            waveform,
            speedMult=studySpeed,
            verbose=CONFIG["verbose"]),
            channel=4
        )

    else:

        if CONFIG["verbose"] == True:
            print("Mode: Break")

        strip.setPalette(breakPal)
        strip.setChannelFunction(createWaveFunction(
            waveform,
            speedMult=breakSpeed,
            verbose=CONFIG["verbose"]),
            channel=4
        )

    return CONFIG



def main():

    with open(r'config.yaml') as file:
        CONFIG = yaml.load(file, Loader=yaml.FullLoader)

    # Settings
    SHORT_ARGS = "vtqr"
    LONG_ARGS  = ["verbose", "test", "quickchange", "rainbow"]

    # Import arguments
    try:
        args, arg_values = getopt.getopt(
            sys.argv[1:],
            SHORT_ARGS,
            LONG_ARGS
        )
    except getopt.error as err:
        # Output error, and return with an error code
        print (str(err))
        sys.exit(2)

    # Change settings off of arguments
    for arg, val in args:

        if arg in ("-v", "--verbose"):
            print("Verbose mode enabled!")
            CONFIG["verbose"] = True

        if arg in ("-t", "--test"):
            print("Hot swap testing enabled!")
            CONFIG["hotswap"] = True

        elif arg in ("-q", "--quickchange"):
            print("Quickchange enabled!")
            CONFIG["check-frames"] = 100

        elif arg in ("-r", "--rainbow"):
            print("Nochange enabled!")
            CONFIG["no-change"] = True

    # Attempt to instantiate the lightstrip.
    try:
        strip = ls.LightStrip(cfg.LED_COUNT)
    except Exception:
        print(
            "An error occurred while setting up the "
            "light strip. Ensure you're running the "
            "setup as the superuser."
        )

    # Initialize strip with default values
    strip.setStepMode(strip.MODE_PALETTE)
    strip.setPalette(pal.DEFAULT_PALETTE)
    strip.setBrightness(0.01)

    config = updateParams(strip, CONFIG, hotswap=True)

    # Instantiate the counter.
    c = 0

    try:

        while True:

            if c % CONFIG["check-frames"] == 0:
                CONFIG = updateParams(
                    strip, 
                    CONFIG, 
                    hotswap=CONFIG["hotswap"]
                )
                print("Checked!")

            strip.step()
            strip.show()

            # Increment counter
            c += 1

    except KeyboardInterrupt:
        strip.clear()
        strip.show()
        print("Stopping...")

# Main entry
if __name__ == "__main__":
    main()
