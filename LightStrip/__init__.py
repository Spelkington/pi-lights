from rpi_ws281x import *
from . import config as cfg
import ctypes, os
import math

class LightStrip():
    """ 
    A convenient wrapper class for the NeoPixel LED strip object. Provides
    additional functionality and the wonderful conveniences of working in 
    Python.

    author: Spencer Elkington
    date:   August 2020
    email:  spelkington@gmail.com
    """


    def __init__ (self,
                  num_pixels    = cfg.LED_COUNT,
                  gpio_pin      = cfg.LED_GPIO_PIN,
                  freq_hz       = cfg.LED_FREQ_HZ,
                  dma           = cfg.LED_DMA,
                  brightness    = cfg.LED_BRIGHTNESS,
                  invert_logic  = cfg.LED_INV_LOGIC,
                  channel       = cfg.LED_CHANNEL):
        """
        Creates a new LightStrip object to represent an LED strip
        attached to the Pi.

        :param numPixels:    An integer value representing the number of pixels attached to
                            the LED strip.
        :param freq_hz:      The frequency of the lights on the strip. Default is 800kHz,
                            which is the most common value.
        :param dma:          DMA. Not really sure what this is, but 10 sure does seem to work.
        :param brightness:   The max brightness value for the LEDs on the strip. Default is 255.
        :param invert_logic: Set to true if a logic inverter is used between the Pi and the data
                            wire of the LED lights. Defaults to false.
        :param channel:      Channel for the LED lights. Defaults to 0.

        """

        if os.getuid() != 0:
            raise Exception("You must run this program as sudo!")
        
        # Instantiate the light strip using the given parameters
        self.strip = Adafruit_NeoPixel(
                                        num_pixels,
                                        gpio_pin,
                                        freq_hz,
                                        dma,
                                        invert_logic,
                                        brightness,
                                        channel
                                      )

        # Save the length of the strip internally
        self.length = num_pixels

        # Set everything we need for the internals of the light.
        self._setup()

        # Allocate the memory for the strip.
        self.strip.begin()

        return

    def _setup (self):
        """
        Sets up the LightStrip with self values and default channel functions for visualization.
        """

        # Set up enumerations for channel values
        self.CH_RED   = 0
        self.CH_GREEN = 1
        self.CH_BLUE  = 2
        self.NUM_CHANNELS  = 3

        return

    def __len__ (self):
        """
        Retrieves the length of the LightStrip in pixels.
        """
        return self.length

    def show (self):
        """
        Pushes display changes to the physical LED strip.
        """
        self.strip.show()
        return

    def _getNEOColorTuple(self, color):
        """
        Converts a NeoPixel Color object (stored as a 32-bit integer) into
        a tuple of RGB values.

        :param color:   A NeoPixel color object (32-bit integer)
        :return:        A 3-number tuple with the (R, G, B) values of the
                        input color
        """

        # Because NeoPixel stores their color values as a single integer, we
        # need to bitshift in order to get them out. These operations:
        #   First, mask the bits that we don't need to 0
        #   Second, bitshift the number until the color value is in the LSBs
        r = (color & 0xff0000) >> 16
        g = (color & 0x00ff00) >> 8
        b = (color & 0x000044) >> 0

        return (r, g, b)


    def _createColor(self, colorTuple):
        """
        Converts an RGB tuple to a NeoPixel color object. Clamps any values outside of [0, 255]
        into range.

        :param colorTuple:  An (R, G, B) tuple with any values.
        :return:            The valid NeoPixel color object representing the input tuple.
        """

        # To sanitize the input color, we use the max-min method to clamp numbers between
        # values of 0 and 255, inclusive.
        return Color(
                int(max(0, min(255, colorTuple[0]))),
                int(max(0, min(255, colorTuple[1]))),
                int(max(0, min(255, colorTuple[2])))
               )


    def fill(self, color):
        """
        Fills the entire strip with a single color.

        :param color:   An (R, G, B) color tuple.
        """
        color = self._createColor(color)
        for i in range(len(self)):
            self.strip.setPixelColor(i, color)

        return


    def clear(self):
        """
        Clears the entire strip by filling all pixels with (0, 0, 0)
        """

        self.fill((0, 0, 0))
        return


    def __getitem__ (self, key):
        """
        Retrieves an color, or set of colors, from the data of the LightStrip.

        :param key: the specified index or indices to be retrieved.
        :return: a color or set of colors from the LightStrip.
        """

        if isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            return [self[i] for i in range(start, stop, step)]

        elif isinstance(key, int):
            return self._getNEOColorTuple(self.strip.getPixelColor(key))

        elif isinstance(key, tuple):
            raise NotImplementedError('Tuple as index')

        else:
            raise TypeError('Invalid Argument Type: {}'.format(type(key)))

        return


    def __setitem__ (self, key, color):
        """
        Sets the value at an index or a range of indices to an (R, G, B) color tuple.

        :param key: an index or range of indices to set
        :param color:   an (R, G, B) color value
        """

        color = self._createColor(color)

        if isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            for i in range(start, stop, step):
                self.strip.setPixelColor(i, color)

        elif isinstance(key, int):
            self.strip.setPixelColor(key, color)

        elif isinstance(key, tuple) or isinstance(key, list):
            for i in key:
                self.strip.setPixelColor(i, color)

        else:
            raise TypeError('Invalid Argument Type: {}'.format(type(key)))

        return

    def setBrightness(self, val):
        self.strip.setBrightness(int(val * 100))
        return